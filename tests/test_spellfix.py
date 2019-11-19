import pytest
import os

def test_script(monkeypatch):
    os.system("python make_names.py")
    # test quit
    monkeypatch.setattr('builtins.input', lambda: 'Q')
    os.system("python spellfix.py")
    # make sure the right files got created/saved
    assert os.path.exists('words.txt')
    
