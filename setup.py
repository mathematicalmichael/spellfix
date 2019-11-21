from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

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
    setup_requires=['pytest', 'codecov', 'pytest-cov'],
    py_modules=['make_names'],
    packages=find_packages()
)
