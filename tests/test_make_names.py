import make_names as mkn
import os
import pytest
from faker import Factory
faker = Factory.create()

def test_delete_char():
    # test that wrong type throws error.
    with pytest.raises(TypeError):
        mkn.delete_char(1)
    # run 100 times just to be sure.
    for _ in range(100):
        name = faker.company()
        target_len = len(name) - 1
        assert len(mkn.delete_char(name)) == target_len

def test_swap_chars():
    # test that wrong type throws error.
    with pytest.raises(TypeError):
        mkn.swap_chars(1)
    # run 100 times just to be sure.
    for _ in range(100):
        name = faker.company()
        target_len = len(name)
        assert len(mkn.swap_chars(name)) == target_len

def test_shuffle_letters():
    # test that wrong type throws error.
    with pytest.raises(TypeError):
        mkn.shuffle_letters(1)
    # run 100 times just to be sure.
    for _ in range(100):
        name = faker.company()
        target_len = len(name)
        assert len(mkn.shuffle_letters(name)) == target_len

def test_chop_letter():
    # test that wrong type throws error.
    with pytest.raises(TypeError):
        mkn.chop_letter(1)
    # run 100 times just to be sure.
    for _ in range(100):
        name = faker.company()
        chopped = mkn.chop_letter(name)
        assert chopped == name[1:] or \
               chopped == name[:-1]

def test_perturb():
    # don't allow invalid options
    with pytest.raises(ValueError):
        mkn.perturb('abc', -1)
    with pytest.raises(ValueError):
        mkn.perturb('abc', 4)
    # dont allow strings
    with pytest.raises(TypeError):
        mkn.perturb('abc', '0')
    # run tests for each r choice
    for _ in range(100):
        name = faker.company()
        target_len = len(name)
        # delete
        assert len(mkn.perturb(name, 0)) == target_len - 1
        # chop
        chopped = mkn.perturb(name, 3)
        assert chopped == name[1:] or \
               chopped == name[:-1]
        assert len(mkn.perturb(name, 3)) == target_len - 1
        # swap
        assert len(mkn.perturb(name, 1)) == target_len
        # shuffle
        assert len(mkn.perturb(name, 2)) == target_len

        random_choice = mkn.perturb(name)
        assert len(random_choice) == target_len or \
               len(random_choice) == target_len - 1

def test_script():
    os.system("python make_names.py")
