# Grouping contacts
Identifying rows in a CSV file that may represen the same person based on a provided matching type.
It will produce the output in a same CSV format with an unique identifier.
If it's identified as the same person, it will have a same identifier.

# How to run this script
* Install dependencies
```
sudo pip install --upgrade pip
pip install virtualenv
virtualenv python
source python/bin/activate
```
* Run requirement packages
```
pip install -e .
```
* Run this script
```
Usage:
  group_contacts --input=FILE --type=TYPE [--type=TYPE] [--output=FILE] [-h] [--version]

- Options
  -i FILE --input=FILE              CSV Format of file required
  -t TYPE --type=type               Matching type or types, repeatable options with an `email` and `phone`
  -o FILE --output=file             Output file path and name [default: ./data/output.csv]
  -h --help                         Show this screen.
  --version                         Show version.

Example:
  # find an `email` type matching
  group_contacts -i data/input1.csv -t email
  -> this will produce the output.csv in ./data directory
  # find an `phone` type matching
  group_contacts -i data/input2.csv -t phone
  # find either `email` or `phone` type matching
  group_contacts -i data/input2.csv -t email -t phone
```

# Future improvement
Need to test it with `python-pandas` module.