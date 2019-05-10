# Calibre Magazine Importer

a script to import digital magazines into Calibre

## Description

_Calibre Magazine Importer_ is a script to import digital magazines into a Calibre library.

It uses the fact that the magazines use filenames that have a fixed and a variable part. The fixed
part can be used to identify the series, authors and publisher. The variable part follows a pattern
from which information can be extracted to calculate the issue's volume, index and release date.

## License

_Calibre Magazine Importer_ is distributed under the
[Mozilla Public License Version 2.0](LICENSE.md).

## Requirements

Without Calibre it doesn't make sense to run the magazine importer. Calibre must be installed,
properly configured and have a database.

The _Calibre Magazine Importer_ script itself is written in Python 3. At least version 3.6 must be
installed. Also the following Python modules must be available:

* TODO

## Installation and Configuration

### Installation

The best way to install _Calibre Magazine Importer_ is to install it in a Python virtual
environment using pip. With a symbolic link in a directory in the path to the
`calibre-magazine-importer` executable, the tool is also available without manually activating the
virtual environment.

1. First, clone the git repository into a local directory. Let's call this `git-dir`.
2. Create a virtual environment where you want to install _Calibre Magazine Importer_  
`python3 -m venv <install-dir>`
3. Activate the virtual environment  
`source <install-dir>/bin/activate`
4. Install _Calibre Magazine Importer_ using pip  
`pip install <git-dir>`
5. Create a symbolic link in a directory on the path (here `/usr/local/bin`)  
`ln -s <install-dir>/bin/calibre-magazine-importer /usr/local/bin/calibre-magazine-importer`

### Configuration

TODO

## Usage

_Calibre Magazine Importer_ is a command line tool. Its syntax is:

```bash
calibre-magazine-importer [-h] [-c CONFIG] [-v]
```

The optional arguments are:

| option | description |
|--------|-------------|
| `-h, --help` | show this help message and exit |
| `-c CONFIG, --config CONFIG` | configuration file for the importer (default: `$HOME/.calibre-magazine-importer`) |
| `-v, --verbose` | be more verbose about the magazines that are imported |

## Changes / History

TODO
