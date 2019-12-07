# spellfix
A typo correction command-line program written in Python.

## status
Master:
[![codecov](https://codecov.io/gh/mathematicalmichael/spellfix/branch/master/graph/badge.svg)](https://codecov.io/gh/mathematicalmichael/spellfix)
[![Build Status](https://travis-ci.com/mathematicalmichael/spellfix.svg?branch=master)](https://travis-ci.com/mathematicalmichael/spellfix)

Develop:
[![codecov](https://codecov.io/gh/mathematicalmichael/spellfix/branch/develop/graph/badge.svg)](https://codecov.io/gh/mathematicalmichael/spellfix)
[![Build Status](https://travis-ci.com/mathematicalmichael/spellfix.svg?branch=develop)](https://travis-ci.com/mathematicalmichael/spellfix)


## installation

```sh
git clone https://github.com/mathematicalmichael/spellfix.git
cd spellfix
pip install .
```

### optional Tf-Idf suggestions
```sh
pip install numpy cython
pip install .[recommend]
```

### optional testing dependencies
```sh
pip install .[testing]
```

That should do it, and you can always use the syntax `pip install -e .`, which will install a development version (as opposed to linking to compiled binaries).

## usage

Let's say you have a file named `wordlist.txt` with a list of names you need to sort through.

If you instead have a CSV with counts, called `wordlist.csv`, where the first column is name and second column has frequency counts (such as those from `groupby`,  run

```sh
python convert csv_to_unknown_json.py -f wordlist.csv
```

as a pre-processing step.
This sets up a dictionary based on those counts for use in `spellfix.py`. 
It also creates the expected `wordlist.txt` file by stripping the second column.
**Make sure that there is no header in the CSV**


If you have the suggestions module, run

```sh
python suggest.py -f wordlist.txt
```

To generate a `wordlist-suggestions.json` file for use in `spellfix.py`, based on TF-iDF with ngrams. 

If these files are missing, `spellfix.py` will do what it can starting from a bare `.txt` file, but will be less good at making suggestions because of its use of Levenshtein distance (of 2) as a threshold for corrections. 
Complicated changes won't be suggested, hence the `suggest.py` module.

Now you can run

```sh
python spellfix.py -f wordlist.txt
```

and use the interactive menu. Pressing `Enter` will perform the same function as `S`, saving. 

When corrections are made or words are added, extra weight is assigned to them in order to aid automatic decision making.
When probabilities are sufficiently high and possible choices sufficiently low, the algorithm will make the choice on your behalf. 

The default action of the `spellfix` module is to run `correct()`, in an attempt to build the dictionary of corrections.

When you save, you'll be able to "hot start" from the files.
You will see files prepended with the name of your original list.


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
