__author__ = 'Arkan'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'FTB modpack fetching library.',
    'author': 'Arkan',
    'author_email': 'arkan@drakon.io',
    'version': '0.0.1',
    'packages': ['libftb'],
    'name': 'LibFTB'
}

setup(**config)