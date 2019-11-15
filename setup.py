from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

about = """
Command-line utility for interactively correcting typos that
occur in a word list.
"""
setup(
    name='fixspell',
    version='0.1',
    description=about,
    author='Michael Pilosov',
    company='Slalom Build',
    author_email='consistentbayes@gmail.com',
    install_requires=requirements
)
