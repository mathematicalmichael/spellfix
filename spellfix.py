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

class Fixer(object):
    def __init__(self, filename):
        self.known_file = 'known_words.txt'
        self.unknown_file = 'unknown_words.txt'
        known = SpellChecker()        
        unknown = SpellChecker()
        self.known = wipe_dictionary(known)
        self.unknown = wipe_dictionary(unknown)
        self.unknown.word_frequency.load_text_file(filename)

menu = """
C. Correct a word. 
Q. Quit/Exit.
S. Save files to disk.
E. Edit existing entries.
K: See known list.
U: See unknown list.
"""

def get_counts(fix):
    """
    Return counts for number of known and unknown words.
    
    Parameters
    ---
    
    Fixer fix: instance of Fixer class.

    Returns
    ---
    (known_count, unknown_count): tuple of integers
    """
    known = fix.known.word_frequency.unique_words
    unknown = fix.unknown.word_frequency.unique_words
    return (known, unknown)

def main(fix):
    """
    Interactive Program for editing typos
    """
    live = 1
    while live:
        counts = get_counts(fix)
        print("=====================")
        print("Done: %d, Remaining: %d"%(counts))
        print(menu)
        choice = input("Make choice from menu: ").lower()
        if choice in ['0', 'Q', 'q']:
            live = 0
            print("Exiting...")
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
