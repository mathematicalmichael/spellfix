#!/usr/env/python
from spellchecker import SpellChecker

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

import fileinput
def pre_process_file(filename):
    fin = open(filename)
    fout = open("words.txt", "wt")
    for line in fin:
        newline = line.lower().replace(' ', '').replace('\'','').replace(',','').replace('-','')
        fout.write(newline)
    fin.close()
    fout.close()


class Fixer(object):
    def __init__(self, filename):
        self.known_file = 'known_words.txt'
        self.unknown_file = 'unknown_words.txt'
        self.corrections = {}
        known = SpellChecker()        
        unknown = SpellChecker()
        self.known = wipe_dictionary(known)
        self.unknown = wipe_dictionary(unknown)
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
        uwfq = self.unknown.word_frequency
        kwfq = self.known.word_frequency
        unknown_words = list(uwfq.dictionary.keys())
        word = unknown_words[0]
        self.unknown.word_frequency.pop(word)
        print("\t===> %s"%word)
        known_candidates = list(self.known.candidates(word))
        unknown_candidates = list(self.unknown.candidates(word))
        # remove word from known candidate list if theere.
        if word in known_candidates:
            known_candidates.remove(word)

        if known_candidates is not None:
            candidates = known_candidates + \
                     unknown_candidates
        else: # no known candidates = empty list.
            candidates = unknown_candidates
            known_candidates = []

        i = 1
        print("0: No mistake. Add word.")
        print("Known:")
        for w in known_candidates:
            print("%d: %s"%(i, w))
            i += 1
        print("Unnown:")
        for w in unknown_candidates:
            print("%d: %s"%(i, w))
            i += 1
        choice = None
        while choice not in range(len(candidates)+1):
            try:
                choice = int(input("\nMake your selection: "))
                correction = candidates[choice-1]
                if choice not in range(len(candidates)+1):
                    print("Please make a valid selection.")
            except ValueError:
                print("Please make a valid selection.")
 
        if choice == 0:
            print("Add %s to KNOWN?"%word)
            ans = get_yn()
            if ans:
                kwfq.add(word)
                uwfq.remove(word)
                self.corrections[word] = []
                print("Added word.")
        else:
            print("Correct %s ===> %s ?"%(word, correction))
            ans = get_yn()
            if ans:
                kwfq.add(correction)
                uwfq.remove(word)
                print("Added correction.")
                self.corections[correction].append(word)
                # to-do: get rid of other instances.
        print(uwfq.unique_words, kwfq.unique_words)

    def save(self):
        """
        """
        pass

def get_yn():
    loop = 1
    while loop:
        choice = input("Confirm (Y/N):")
        if choice in ['y', 'Y', '1']:
            return True
        elif choice in ['n', 'N', '0']:
            return False
        else:
            print("Invalid choice. Please try again.")

menu = """
C. Correct a word. 
Q. Quit/Exit.
S. Save files to disk.
E. Edit existing entries.
K: See known list.
U: See unknown list.
"""

def main(fix):
    """
    Interactive Program for editing typos
    """
    live = 1
    while live:
        counts = fix.get_counts()
        print("=====================")
        print("Done: %d, Remaining: %d"%(counts))
        print(menu)
        choice = input("Make choice from menu: ").lower()
        # quit
        if choice in ['0', 'Q', 'q']:
            live = 0
            print("Exiting...")
        # correct   
        elif choice in ['C', 'c']:
            fix.correct()
        # save
        elif choice in ['S', 's']:
            fix.save()
        # edit
        elif choice in ['E', 'e']:
            continue
        # see knowns
        elif choice in ['K', 'k']:
            k = fix.show_known()
            print(k)
        # see unknowns
        elif choice in ['U', 'u']:
            u = fix.show_unknown()
            print(u)
        else:
            print("Choice not understood. Please try again.")
            continue
 
    return None

if __name__ == '__main__':
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
        raise ValueError(f"File {filename} does not exist.")
    fix = Fixer(filename)
    main(fix)
