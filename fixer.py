#!/usr/env/python
from spellchecker import SpellChecker

def wipe_dictionary(spell:SpellChecker):
    """
    The dictionary attribute is "not settable" by design.
    Thus, we need to manually remove all the words from it
    in order to empty its contents.
    """
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
        self.known.word_frequency.load_text_file(filename)

if __name__ == '__main__':
    import argparse
    desc = "Typo Corrector!"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-f', '--file',
                        default='wordlist.txt',
                        type=str,
                        help='File name of words to correct.')
    args = parser.parse_args()
    filename = args.file
    fix = Fixer(filename)
    print(fix.known.word_frequency.unique_words)
    print(fix.unknown.word_frequency.unique_words)
