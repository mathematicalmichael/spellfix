import re
import os
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from scipy.sparse import csr_matrix
import sparse_dot_topn.sparse_dot_topn as ct
from spellfix import format_str

def ngrams(string, n=3):
    string = format_str(string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]


def awesome_cossim_top(A, B, ntop, lower_bound=0):
    # force A and B as a CSR matrix.
    # If they have already been CSR, there is no overhead
    A = A.tocsr()
    B = B.tocsr()
    M, _ = A.shape
    _, N = B.shape
 
    idx_dtype = np.int32
 
    nnz_max = M*ntop
 
    indptr = np.zeros(M+1, dtype=idx_dtype)
    indices = np.zeros(nnz_max, dtype=idx_dtype)
    data = np.zeros(nnz_max, dtype=A.dtype)

    ct.sparse_dot_topn(
        M, N, np.asarray(A.indptr, dtype=idx_dtype),
        np.asarray(A.indices, dtype=idx_dtype),
        A.data,
        np.asarray(B.indptr, dtype=idx_dtype),
        np.asarray(B.indices, dtype=idx_dtype),
        B.data,
        ntop,
        lower_bound,
        indptr, indices, data)

    return csr_matrix((data,indices,indptr),shape=(M,N))


def get_matches_df(sparse_matrix, name_vector, top=100):
    non_zeros = sparse_matrix.nonzero()
    
    sparserows = non_zeros[0]
    sparsecols = non_zeros[1]
    
    if top:
        nr_matches = top
    else:
        nr_matches = sparsecols.size
    
    left_side = np.empty([nr_matches], dtype=object)
    right_side = np.empty([nr_matches], dtype=object)
    similairity = np.zeros(nr_matches)
    
    for index in range(0, nr_matches):
        left_side[index] = name_vector[sparserows[index]]
        right_side[index] = name_vector[sparsecols[index]]
        similairity[index] = sparse_matrix.data[index]
    
    return pd.DataFrame({'left_side': left_side,
                          'right_side': right_side,
                           'similarity': similairity})


def names_from_file(filename='wordlist.txt', header=None):
    names = pd.read_table(filename, header=header)
    names.columns = ['Company Name']
    company_names = names['Company Name'].unique()
    return company_names

def make_matches(company_names, ntop=10, thresh=0.50):
    """
    Use scikit-learn's `TfidVectorizer` to embed into word-space.
    """
    vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
    tf_idf_matrix = vectorizer.fit_transform(company_names) 
    matches = awesome_cossim_top(tf_idf_matrix, tf_idf_matrix.transpose(), ntop=ntop, lower_bound=thresh)
    return matches 


def groupings_to_file(grouped_df, foldername='matches', ftype='json'):
    """
    Dump results of df.groupby() to a folder.
    Each group gets its own CSV file without indices or headers.
    """
    if ftype == 'csv':
        if not os.path.exists(foldername+'-matches'):
            os.mkdir(foldername)
        else:
            os.system('rm {}/*'.format(foldername+'-matches'))
    D = {} 
    for k, gr in grouped_df:
        print("Processing {}".format(k))
        fname = format_str(k)
        tmp_df = gr['right_side'].apply(lambda x: format_str(x))
        if ftype == 'csv':
            tmp_df.to_csv('{}/{}.csv'.format(foldername+'-matches', fname), index=False, header=False )
        
        D[format_str(k)] = tmp_df.tolist()
    with open(foldername+'-suggestions.json','w') as f:
        json.dump(D,f)
    group_counts = grouped_df.count()
    group_counts.to_csv('{}-groups.csv'.format(foldername), header=False)
    return group_counts


##########

def main(fname):
    company_names = names_from_file(fname)
    matches = make_matches(company_names)
    matches_df = get_matches_df(matches, company_names, top=None)
    matches_df = matches_df[matches_df['similarity'] < 0.99999] # Remove all exact matches
    
    samps_sorted = matches_df.sort_values(['similarity'], ascending=False)
    lgrouped = samps_sorted[['left_side', 'right_side']].groupby('left_side', sort=True)
    prefix = fname.replace('.csv', '').replace('.txt', '')
    group_counts = groupings_to_file(lgrouped, prefix) 

    return group_counts

if __name__ == '__main__':
    import argparse
    import os
    desc = "Generate suggestions for possible corrections."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-f', '--file',
                        default='wordlist.txt',
                        type=str,
                        help='File name of words to correct.')
    args = parser.parse_args()
    filename = args.file
    if not os.path.exists(filename):
        raise ValueError("File %s does not exist."%filename)
    group_counts = main(filename)
    print(group_counts)

