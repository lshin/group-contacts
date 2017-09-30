"""Packaging settings."""
from setuptools import Command, find_packages, setup
from src import __version__

setup(
    name = 'Grouping contacts',
    version = __version__,
    description = 'A command line tool that generating a csv file with unique identifier and list after finding same data with matching field(s)',
    author = 'Leo Shin',
    author_email = 'leo@sh1n.com',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt', 'schema', 'hashids'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'group_contacts=src.group_contacts:main',
        ],
    }
)