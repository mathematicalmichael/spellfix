from setuptools import setup, find_packages
import traceback

extra_params = {}
setup_requires = ['pytest', 'codecov', 'pytest-cov']
try:
    import pip
    pip.main(['install'] + setup_requires)
    setup_requires = []
except Exception:
    # Going to use easy_install for
    traceback.print_exc()

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
    setup_requires=setup_requires,
    extras_require={
        'recommend': recommend,
    },
    py_modules=['make_names'],
    packages=find_packages()
)
