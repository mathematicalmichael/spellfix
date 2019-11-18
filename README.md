# spellfix

Master:
[![codecov](https://codecov.io/gh/mathematicalmichael/spellfix/branch/master/graph/badge.svg)](https://codecov.io/gh/mathematicalmichael/spellfix)
[![Build Status](https://travis-ci.com/mathematicalmichael/spellfix.svg?branch=master)](https://travis-ci.com/mathematicalmichael/spellfix)

Develop:
[![codecov](https://codecov.io/gh/mathematicalmichael/spellfix/branch/develop/graph/badge.svg)](https://codecov.io/gh/mathematicalmichael/spellfix)
[![Build Status](https://travis-ci.com/mathematicalmichael/spellfix.svg?branch=develop)](https://travis-ci.com/mathematicalmichael/spellfix)

A typo correction command-line program written in Python.

## installation

```sh
git clone https://github.com/mathematicalmichael/spellfix.git
cd spellfix
pip install .
```

should do it, and `pip install -e .` will install a development version.

## docs

`python spellfix.py --help`

`python make_names.py --help`

## usage

Generate a file of names (if you don't have your own), and call it `wordlist.txt`, which the program looks for by default.

`python make_names.py`

Then, you can run 
`python spellfix.py`

If you want to specify your own file:
`python spellfix.py -f FILE`
