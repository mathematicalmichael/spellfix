from setuptools import setup, find_packages
import traceback

extra_params = {}
setup_requires = ['pytest', 'codecov', 'pytest-cov']

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('recommended_requirements.txt') as f:
    recommend = f.read().splitlines()
 
about = """
Command-line utility for interactively correcting typos that
occur in a word list.
"""
setup(
    name='spellfix',
    version='0.1',
    description=about,
    author='Michael Pilosov',
    company='Slalom Build',
    author_email='consistentbayes@gmail.com',
    install_requires=requirements,
    extras_require={
        'recommend': recommend,
        'testing': setup_requires,
    },
    py_modules=['make_names', 'spellfix'],
    packages=find_packages()
)
