import pandas as pd
from spellfix import format_str
import json
def main(filename):
    a = pd.read_csv(filename, header=None)
    a[0] = a[0].apply(lambda x: format_str(x))
    a = a.set_index([0])
    d = a.to_dict()[1]
    filename=filename.replace('.csv','').replace('-groups','')
    with open('%s-unknown_words.json'%filename, 'w') as f:
        json.dump(d, f)
    with open('%s.txt'%filename, 'w') as f:
        f.write('\n'.join(list(d.keys())))

if __name__ == '__main__':
    import argparse
    import os
    desc = "Turn groupings CSV into JSON"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-f', '--file',
                        default='wordlist-groups.csv',
                        type=str,
                        help='File name of groupings.')
    args = parser.parse_args()
    filename = args.file
    if not os.path.exists(filename):
        raise ValueError('File %s does not exist.'%filename)
    else:
        main(filename)
