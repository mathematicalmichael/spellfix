#!/usr/env/python
import re
from spellchecker import SpellChecker

def format_str(word):
        return re.sub(r'[,-./]|\sExt',r'', word).replace(' ', '_').lower()

def wipe_dictionary(spell):
    """
    The dictionary attribute is "not settable" by design.
    Thus, we need to manually remove all the words from it
    in order to empty its contents.
    """
    if not isinstance(spell, SpellChecker):
        raise TypeError("Please pass a SpellChecker object")
    d = spell.word_frequency.dictionary
    spell.word_frequency.remove_words(list(d.keys()))
    return spell

def pre_process_file(filename):
    fin = open(filename)
    fout = open("words.txt", "wt")
    for line in fin:
        #newline = line.lower().replace(' ', '').replace('\'','').replace(',','').replace('-','')
        newline = format_str(line)
        fout.write(newline)
    fin.close()
    fout.close()


class Fixer(object):
    def __init__(self, filename):
        self.known_file = 'known_words.txt'
        self.unknown_file = 'unknown_words.txt'
        self.corrections = {}
        self.known = SpellChecker(distance=2, language=None, case_sensitive=False)
        self.unknown = SpellChecker(distance=2, language=None, case_sensitive=False)        
        #self.known = wipe_dictionary(known)
        #self.unknown = wipe_dictionary(unknown)
        pre_process_file(filename)
        self.unknown.word_frequency.load_text_file('words.txt')

    def get_counts(self):
        """
        Return counts for number of known and unknown words.
        
        Returns
        ---
        (known_count, unknown_count): tuple of integers

        """
        known = self.known.word_frequency.unique_words
        unknown = self.unknown.word_frequency.unique_words
        return (known, unknown)

    def show_known(self):
        """
        """
        return self.known.word_frequency.dictionary

    def show_unknown(self):
        """
        """
        return self.unknown.word_frequency.dictionary

    def correct(self):
        """
        """
        quit = False
        uwfq = self.unknown.word_frequency
        kwfq = self.known.word_frequency
        unknown_words = list(uwfq.dictionary.keys())
        word = unknown_words[0]
        #self.unknown.word_frequency.pop(word)
        # uwfq.remove(word)
        print("\t===> %s"%word)
        # TODO: COMPLETELY CHANGE THE CANDIDATE GENERATION
        known_candidates = list(self.known.candidates(word))
        unknown_candidates = list(self.unknown.candidates(word))
        fname = 'matches/' + format_str(word) + '.csv'
        try:
            with open(fname, 'r') as f:
                loaded_options = f.read().splitlines()
            # clean up duplicates from loaded list.
            for w in known_candidates:
               if w in loaded_options:
                    loaded_options.remove(w) 
            unknown_candidates += loaded_options
        except FileNotFoundError: # sometimes the TFidF doesn't match words
            loaded_options = []

        #print(known_candidates, unknown_candidates)
        # remove word from known candidate list if there.
        if word in kwfq.dictionary:
            print("Word already seen.") 
            uwfq.remove(word)
            print("Removed from unknown list.")
        else:  # word not known. make decision
            for w in known_candidates:
                if w in unknown_candidates:
                    unknown_candidates.remove(w) 
            if word in known_candidates: # spellchecker returns word if not seen instead of empty list.
                known_candidates.remove(word)
            if word in unknown_candidates:
                unknown_candidates.remove(word)
            #print(known_candidates, unknown_candidates)
            candidates = []
            if known_candidates is not None:
                candidates += known_candidates
            else:
                known_candidates = []
            if unknown_candidates is not None:
                candidates += unknown_candidates
            else:
                unknown_candidates = []
    
            choices = [str(s) for s in range(len(candidates)+1)]
            if len(candidates) == 0:
                # no candidates. must be new word.
                # choice is made on your behalf
                if len(candidates) == 0:
                    choice = '0'
                skip = True # skip confirmation
            elif (len(unknown_candidates) == 0) and (len(known_candidates) == 1):
                # one known and no unknowns.
                choice = '1'
                print("Making correction to only known option.")
                skip = True
            else:
                skip = False # do not skip confirmation
                i = 1
                print("0: No mistake. Add word.")
                print("Known:")
                for w in known_candidates:
                    print("%d: %s"%(i, w))
                    i += 1
                print("Unknown:")
                for w in unknown_candidates:
                    print("%d: %s"%(i, w))
                    i += 1
                choice = None
                
                while choice not in choices + ['Q', 'U', 'K', 'L', 'S']:
                    try:
                        choice = input("\nMake your selection: ")
                        if choice not in choices:
                            print("Please make a valid selection.")
                    except ValueError:
                        print("Please make a valid selection.")
        
            if choice == '0':
                if skip:
                    ans = True
                    print("%s appears to be new. Adding."%word)
                else:
                    print("Add %s to KNOWN?"%word)
                    ans = get_yn()
    
                if ans:
                    kwfq.add(word)
                    uwfq.remove(word)
                    self.corrections[word] = []
                    print("Added word.")
            elif choice in choices:
                choice = int(choice) # numerical choice.
                correction = candidates[choice-1]
                if skip:
                    ans = True
                    print("%s appears to be the only candidate correction. Correcting %s."%(correction, word))
                else:
                    print("Correct %s ===> %s ?"%(word, correction))
                    ans = get_yn()
    
                if ans:
                    kwfq.add(correction)
                    if word in uwfq.dictionary:
                        print("Removing word from unknowns.")
                        uwfq.remove(word)
                    if correction in uwfq.dictionary:
                        print("Removing correction from unknowns.")
                        uwfq.remove(correction)
                    print("Added correction.")
                    # if first time adding alias, initialize list.
                    if correction not in self.corrections:
                        self.corrections[correction] = []
                    self.corrections[correction].append(word)
                    # to-do: get rid of other instances.
            else:
                quit = select_option(self, choice)
            return quit

    def save(self):
        """
        """
        print("SAVE!") 
        pass

    def show_corrections(self):
        """
        """
        return self.corrections

def get_yn():
    loop = 1
    while loop:
        choice = input("Confirm (Y/N):")
        if choice in ['y', 'Y', '1', '']:
            return True
        elif choice in ['n', 'N', '0']:
            return False
        else:
            print("Invalid choice. Please try again!\n")

menu = """
C. Correct a word. 
Q. Quit/Exit.
S. Save files to disk.
E. Edit existing entries.
K: See known list.
U: See unknown list.
L: See corrections list.
"""

def select_option(fix, choice):
    quit = False
    # quit
    if choice in ['0', 'Q', 'q']:
        quit = True
        print("Exiting...")
    # correct   
    elif choice in ['C', 'c', '']:  # default choice
        fix.correct()
    # save
    elif choice in ['S', 's']:
        fix.save()
    # edit
    elif choice in ['E', 'e']:
        pass
    # see knowns
    elif choice in ['K', 'k']:
        k = fix.show_known()
        print(k)
    # see unknowns
    elif choice in ['U', 'u']:
        u = fix.show_unknown()
        print(u)
    elif choice in ['L', 'l']:
        l = fix.show_corrections()
        print(l)
    else:
        print("Choice not understood. Please try again.")
        pass
    return quit
 
def mainmenu(fix):
    """
    Interactive Program for editing typos
    """
    quit = False
    while not quit:
        counts = fix.get_counts()
        print("=====================")
        print("Done: %d, Remaining: %d"%(counts))
        print(menu)
        quit = fix.correct()

        #choice = input("Make choice from menu: ")
    
    return None

def main():
    import argparse
    import os
    desc = "Typo Corrector!"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-f', '--file',
                        default='wordlist.txt',
                        type=str,
                        help='File name of words to correct.')
    args = parser.parse_args()
    filename = args.file
    if not os.path.exists(filename):
        raise ValueError("File %s does not exist."%filename)
    fix = Fixer(filename)
    mainmenu(fix)

if __name__ == '__main__':
    main()
