"""
Grouping contacts

Usage:
  group_contacts --input=FILE --type=TYPE [--type=TYPE] [--output=FILE] [-h] [--version]

Options:
  -i FILE --input=FILE              CSV Format of file required
  -t TYPE --type=type               Matching type or types, repeatable options with an `email` and `phone`
  -o FILE --output=file             Output file path and name [default: ./data/output.csv]
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  group_contacts
"""
from inspect import getmembers, isclass
from docopt import docopt
from schema import Schema, And, Or, Use, Optional, SchemaError
import os.path
from . import __version__ as VERSION


def main():
    """
    Read all options of commands with docopt
    http://docopt.org/
    """
    options = docopt(__doc__, version=VERSION)
    _validate_schema(options)
    _command_run(options)

def _validate_schema(options):
    """
    Validating a option schema
    """
    schema = Schema({
            '--input': And(Use(open, error='Please check a input file path or file name.')),
            '--type' : And(lambda t: t in [['email'], ['phone'], ['email', 'phone'], ['phone', 'email']], error='A matching type must be `email` or `phone`'),
            Optional('--output') : Use(lambda f: open(f, 'w'), error='Output file should be writable.'),
            Optional('--help') : bool,
            Optional('--version') : bool
        })
    try:
        schema.validate(options)
    except SchemaError as e:
        exit(e)

def _command_run(options):
    import grouping
    module = getattr(grouping, 'contacts')
    commands = getmembers(module, isclass)
    command = [command[1] for command in commands if command[0] != 'Base'][0]
    command = command(options)
    command.run()