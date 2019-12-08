#!/usr/env/python
import os
import random
import re
from spellchecker import SpellChecker
import json

def unique(wordlist):
    return list(set(wordlist))

def format_str(word):
        return re.sub(r'[,-./]|\sExt',r'', word).replace(' ', '_').lower().replace(' ', '')

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
    fout = open("words.txt", "wt") # temporary file for processed words
    for line in fin:
        #newline = line.lower().replace(' ', '').replace('\'','').replace(',','').replace('-','')
        newline = format_str(line)
        fout.write(newline)
    fin.close()
    fout.close()


class Fixer(object):
    def __init__(self, filename):
        """
        
        Parameters
        ----------
          filename: CSV or TXT file, one entry per line.
        """
        self.prefix = filename.replace('.txt', '').replace('.csv', '')
        self.known_file =  self.prefix + '-known_words.json'
        self.unknown_file = self.prefix + '-unknown_words.json'
        self.corrections_file = self.prefix + '-corrections.json'
        if os.path.exists(self.corrections_file):
             with open(self.corrections_file, 'r') as f:
                self.corrections = json.load(f)
        else:
            self.corrections = {}

        self.threshold = 10
        self.suggest = None
        self.suggest_file = self.prefix + '-suggestions.json'
        if os.path.exists(self.suggest_file):
            print("Reading suggestions.")
            with open(self.suggest_file, 'r') as f:
                self.suggest = json.load(f)
        
        self.skipped_file = self.prefix + '-skipped.json'
        if os.path.exists(self.skipped_file):
            print("Reading skipped.")
            with open(self.skipped_file, 'r') as f:
                self.skipped = json.load(f)
        else:
            self.skipped = {}

        self.known = SpellChecker(distance=2, language=None, case_sensitive=False)
        if os.path.exists(self.known_file):
            print("Reading known")
            self.known.word_frequency.load_dictionary(self.known_file)

        self.unknown = SpellChecker(distance=2, language=None, case_sensitive=False)        
        if os.path.exists(self.unknown_file):
            print("Reading unknown")
            self.unknown.word_frequency.load_dictionary(self.unknown_file)
            if not os.path.exists(self.known_file):
                print("Making known by trimming unknown")
                self.known.word_frequency.load_dictionary(self.unknown_file)
                self.known.word_frequency.remove_by_threshold(self.threshold)
                keys = [x for x in self.known.word_frequency._dictionary.keys()]
                for key in keys:
                    wordfreq = self.unknown.word_frequency._dictionary[key]
                    if  wordfreq > self.threshold:
                        print("Removing %s from unknown because above threshold of %d"%(key, self.threshold))
                        self.unknown.word_frequency._dictionary.pop(key)
                self.unknown.word_frequency._update_dictionary()

        else:
            print("Loading file.")
            pre_process_file(filename) # creates a words.txt file for us
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

    def show_skipped(self):
        """
        """
        return self.skipped

    def skip(self):
        """
        Add word to skip list and remove from unknown words.
        """
        print("Skipping %s"%self.word)
        self.skipped[self.word] = self.unknown.word_frequency.dictionary[self.word]
        self.unknown.word_frequency.remove(self.word)

    def dump_skipped(self):
        for word in self.skipped:
            for _ in range(self.skipped[word]):
                self.unknown.word_frequency.add(word)
        print("Dumped skipped back into unknown")

    def correct(self):
        """
        """
        quit = False
        uwfq = self.unknown.word_frequency
        kwfq = self.known.word_frequency
        unknown_words = list(uwfq.dictionary.keys())
        suggest = self.suggest
        
        if len(unknown_words) == 0:
            if len(self.skipped) == 0:
                quit = True
                print("YOU ARE DONE!")
                return quit # FINISHED!
            else:
                print("Almost done! Moving skipped into unknown.")
                self.dump_skipped()
                return quit # CYCLE BACK THROUGH AGAIN
        else:
            r = len(unknown_words)
            word = ''
            self.word = word
            random_choice = False
            if random_choice:
                j = 0 # how many times can we try passing through short words before giving up?
                while (len(word) <= 4) and (j<10):
                    word = unknown_words[random.randint(0,r-1)]
                    j += 1
            else:
                word = unknown_words[0]
                self.word = word # store for reference

        #self.unknown.word_frequency.remove(word)
        # uwfq.remove(word)
        print("\t===> %s"%word)
        known_candidates = list(self.known.candidates(word))
        unknown_candidates = list(self.unknown.candidates(word))
        if word in suggest.keys():
            unknown_candidates += suggest[word]
        # remove duplicates
        unknown_candidates = unique(unknown_candidates)
        known_candidates = unique(known_candidates)

        #print(known_candidates, unknown_candidates)
        # remove word from known candidate list if there.
        if word in kwfq.dictionary:
            print("Word already seen.") 
            uwfq.remove(word)
            print("Removed from unknown list.")
        else:  # word not known. make decision
            if word in known_candidates: # spellchecker returns word if not seen
                known_candidates.remove(word)
            for w in known_candidates:
                if w in unknown_candidates:
                    unknown_candidates.remove(w) 

            to_rm = [] # move unknowns to knowns if they belong there (suggestions)
            for w in unknown_candidates:
                if w in kwfq.dictionary.keys():
                    known_candidates.append(w)
                    to_rm.append(w)
            for w in to_rm:
                unknown_candidates.remove(w)

            if word in unknown_candidates and len(known_candidates) > 0:
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
    
            # build probabilities
            freqs = [uwfq.dictionary[word]]
            freqs += [ kwfq.dictionary[w] for w in known_candidates]
            freqs += [ uwfq.dictionary[w] for w in unknown_candidates]
            tot_words = sum(freqs)
            probs = [f/tot_words for f in freqs]

            choices = [str(s) for s in range(len(candidates)+1)]
            if len(candidates) == 0:
                # no candidates. must be new word.
                # choice is made on your behalf
                if len(candidates) == 0:
                    choice = '0'
                skip = True # skip confirmation
            elif (len(unknown_candidates) == 0) and (len(known_candidates) == 1) and (probs[1] > 2.5*probs[0]):
                # one known and no unknowns, high prob of being other word
                # threshold is "twice as often"
                choice = '1'
                print("Making correction to only known option (higher probability than being new.).")
                skip = True
            elif (len(unknown_candidates) == 0) and (len(known_candidates) == 1) and (probs[0] > 2.5*probs[1]):
                # one known and no unknowns, higher prob of being new
                choice = '0'
                print("Adding word (higher probability of being new).")
                skip = True
            else:
                skip = False # do not skip confirmation
                print("0: No mistake. Add word. %2.2f%%"%(100*probs[0]))
                i = 1
                print("Known:")
                for w in known_candidates:
                    #TODO change probability
                    p = 100*probs[i]
                    print("%d: %s - %2.2f%%"%(i, w, p))
                    i += 1
                print("Unknown:")
                for w in unknown_candidates:
                    p = 100*probs[i]
                    print("%d: %s - %2.2f%%"%(i, w, p))
                    i += 1
                choice = None
                letter_choices =  ['Q', 'P', 'O', 'U', 'K', 'L', 'S']
                all_choices = choices + letter_choices + [s.lower() for s in letter_choices] 
                while choice not in all_choices:
                    choice = input("\nMake your selection: ")
                    if choice == '': # overwriting default
                        choice = 'S'
                    if choice not in all_choices:
                        print("Please make a valid selection.")
        
            if choice == '0': # no mistake
                if skip:
                    ans = True # answer = automate
                    print("%s appears to be new. Adding."%word)
                else:
                    print("Add %s to KNOWN?"%word)
                    ans = get_yn()
    
                if ans:
                    # need to do this for correct frequency counts
                    for _ in range(uwfq.dictionary[word]):
                        kwfq.add(word)
                    # give extra instances because it was added by user
                    for _ in range(5):
                        kwfq.add(word)
                    # remove from unknowns.
                    uwfq.remove(word)
                    #self.corrections[word] = []
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
                    for _ in range(uwfq.dictionary[correction]):
                        kwfq.add(correction) 
                    # absorb frequencies
                    for _ in range(uwfq.dictionary[word]):
                        kwfq.add(correction)
                    print("Added %s to knowns."%correction)
                    if word in uwfq.dictionary:
                        print("Removing %s from unknowns."%word)
                        uwfq.remove(word)
                    if word in self.skipped:
                        self.skipped.remove(word)
                    if correction in self.skipped:
                        self.skipped.remove(correction)
                    if correction in uwfq.dictionary:
                        print("Removing %s from unknowns."%correction)
                        uwfq.remove(correction)

                    # if first time adding alias, initialize list.
                    if correction != word: 
                        if correction not in self.corrections:
                            self.corrections[correction] = []
                            # if first time, give extra emphasis
                            for _ in range(3):
                                kwfq.add(correction)
                        self.corrections[correction].append(word)
                    else: # graceful "error" handling without crashing.
                        print("Correcting word to itself. Adding as new instead.")
                    
                    # go through list and remove words
                    self.clean()        
            else:
                self.word = word
                quit = select_option(self, choice)
            return quit


    def clean(self):
        # we already pulled the suggestions for this word
        # so we can remove it from the dictionary.
        if self.word in self.suggest.keys():
            self.suggest.pop(self.word)
        # now we want to go through the rest of the keys
        # and remove instances of the word that appear
        # as suggestions for other (unseen) words.
        # since we know it is an invalid spelling, 
        # it should not appear anymore as an option
        # which should expedite auto-corrections
        for key in self.suggest.keys():
            if self.word in self.suggest[key]:
                self.suggest[key].remove(self.word)
                    
        if self.word in self.skipped:
            self.skipped.remove(self.word)

    def save(self):
        """
        """
        with open(self.unknown_file, 'w') as f:
            json.dump(self.unknown.word_frequency.dictionary, f)
        with open(self.known_file, 'w') as f:
            json.dump(self.known.word_frequency.dictionary, f)
        with open(self.corrections_file, 'w') as f:
            json.dump(self.corrections, f)
        with open(self.skipped_file, 'w') as f:
            json.dump(self.skipped, f)
        print("SAVED!") 

    def show_corrections(self):
        """
        """
        return self.corrections

def get_yn():
    loop = 1
    while loop:
        choice = input("Confirm ([Y]/N):")
        if choice in ['y', 'Y', '1', '']:
            return True
        elif choice in ['n', 'N', '0']:
            return False
        else:
            print("Invalid choice. Please try again!\n")

menu = """
\tQ. Quit/Exit.
\tP: Skip word.
\tO: Show skipped words.
\tS. Save files to disk.
\tE. Edit existing entries.
\tK: See known list.
\tU: See unknown list.
\tL: See corrections list.
"""

def select_option(fix, choice):
    quit = False
    # quit
    if choice in ['0', 'Q', 'q']:
        quit = True
        fix.save()
        print("Exiting...")
    # skip   
    elif choice in ['P', 'p']:
        fix.skip()
    elif choice in ['O', 'o']:
        fix.show_skipped()
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
    i = 0
    while not quit:
        counts = fix.get_counts()
        print("\n=====================")
        print("Done: %d, Remaining: %d"%(counts))
        print(menu)
        quit = fix.correct()
        i += 1
        if i%20 == 0:
            print("20 iterations automated. Would you like to proceed?")
            choice = input("Make choice from menu: ")
            if choice in ['C', 'c', '']:
                continue
            else:
                quit = select_option(fix,choice) 
    
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
