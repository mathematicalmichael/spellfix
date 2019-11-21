import pytest
import os
import make_names as mkn
import spellfix

def test_script(monkeypatch):
    mkn.main() # make text file
    # test quit
    monkeypatch.setattr('builtins.input', lambda x: 'Q')
    spellfix.main()
    # make sure the right files got created/saved
    assert os.path.exists('words.txt')
    
