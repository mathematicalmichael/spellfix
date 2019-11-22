import pytest
import os
import make_names as mkn
import spellfix

def test_script(monkeypatch):
    mkn.main() # make text file
    # test options
    for opt in ['Q', 'S', 'K', 'U', 'L']:
        monkeypatch.setattr('builtins.input', lambda x: 'Q')
        spellfix.main()
        # make sure the right files got created/saved
        assert os.path.exists('words.txt')
        if opt == 'S':
            assert os.path.exists('wordlist-corrections.json')
            assert os.path.exists('wordlist-known_words.json')
            assert os.path.exists('wordlist-unknown_words.json')
