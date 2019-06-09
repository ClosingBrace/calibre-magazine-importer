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

* parse 1.12

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

_Calibre Magazine Importer_ uses a configuration file in a modified INI-file format. The file starts
with some general settings, after wich sections follow for each magazine that can be imported.

#### General settings

The general settings come before the magazine sections. The settings are:

* **importdir** The directory that contains the files to import.
* **calibredb** (optional) The path to the `calibredb` executable (default: `calibredb`).
* **librarypath** (optional) The path to the calibre library (default: the path stored in Calibre's
                  settings).

#### Magazine sections

Magazine sections use the series' name between square brackets as section header. A section further
contains the following settings:

* **format** A format string for the magazine's filename.
* **authors** A comma separated list of the magazine's authors.
* **languages** (optional) A comma separated list of ISO 639-2 language codes for the languages that
                the magazine is published in (default: None).
* **publisher** The publisher of the magazine.
* **volume** (optional) The magazine's volume number.
* **index** (optional) The index within the volume number.
* **year** (optional) The year of publication.
* **month** (optional) The month of publication.
* **tags** (optional) Tags associated with the magazine (default: None).
* **title** The issue's title.
* **archivedir** (optional) The directory where the magazine will be archived (default: None).

After the magazine has been imported into Calibre, it will be moved to the _archivedir_. When
_archivedir_ is not given, the magazine is deleted.

##### The format string

The specification of the format string is based on the
[parse module](https://pypi.org/project/parse/). The format string consists of fields and literal
text. Fields are written between braces (`{` and `}`) and contain a field name and format
specification separated by a `:`. To match a brace in the filename, write a double-brace (`{{` or
`}}`) in the format string.

The format specification is the same as for the [parse module](https://pypi.org/project/parse/), but
typically only a small subset is used. In the common cases a number is given for the number of
characters to match, followed by a `d` to match only digits, a `w` to match only letters, numbers or
underscore, or nothing to match any character.

The following field names are recognized by _Calibre Magazine Importer_:
* **V** The issue's volume number.
* **I** The index within the issue's volume number.
* **Y** The year of publication in two or four digits.
* **M** The month of publication, either as a number, a three letter abreviation or the full month.
Any other field name, or unnamed fields, can be used to capture a non-fixed text sequence that will
be discarded.

##### The volume, index, year and month

The optional _volume_, _index_, _year_ and _month_ contain formulas to calculate the volume, index,
year and month from fields captured from the filename. First _V_, _I_, _Y_ and _M_ are converted to
integers. If _Y_ is a two-digit year, 2000 is added to it. If _M_ is an (abbreviated) month, it is
converted to a number in the range 1 to 12 corresponding to the month. If one of the fields _V_,
_I_, _Y_ or _M_ is not set by parsing the filename, it is initialized to 0. After these conversions,
the formulas are applied. Use `//` in the formulas for integer division. If the configuration does
not contain a formula to calculate one of the fields _volume_, _index_, _year_ or _month_, that
field will be initialized with the value from its matching _V_, _I_, _Y_ or _M_.

##### The title

The _title_ contains a format string in the usual python
[format string syntax](https://docs.python.org/3/library/string.html#formatstrings), with the
restriction that the replacement fields must contain a field name. The available field names are
*volume*, *index*, *year*, *month* and *next_month*. *volume*, *index*, *year* and *month* have the
same meaning as in the configuration file. *next_month* is the month immediately following *month*.
All five field names can be used without format specifiers or with format specifiers for integers.
Next to that, *month* and *next_month* can also be used with format specifiers for strings. By
default, when *month* or *next_month* is used, it will give the month as a number. When the format
specifier ends with an 's', the *month* or *next_month* will give the month's name.

##### Security considerations

The _format_ and _title_ are directly passed on to the parse- and format-functions. _volume_,
_index_, _year_ and _month_ contain expressions that are evaluated with python's **eval** function.
These can provide a security risk when the program execution and the configuration file are not
under the user's control (the program is executed in the user's context; no elevated permission are
needed or requested).

#### Example

Following is an example configuration file for two magazines.
* _Great Magazine_ appears every month, starting in 2011.
* _Super Magazine_ appears every other month, starting in 2006.

```ini
importdir = ~/Downloads

[Great Magazine]
format = gm-{M:3}{Y:2d}.pdf
authors = Great Authors
languages = eng
publisher = The Great Company
volume = Y - 2010
index = M
tags = Magazine,Great
title = Great Magazine {month:s} {year}
archivedir = ~/archive/Great_Magazine

[Super Magazine]
format = super-{V:d}.{I:d}.pdf
authors = The authors
languages = eng,nld
publisher = Super Publishing
year = V + 2005
month = 2 * I - 1
tags = Magazine,Super,Bimonthly
title = Super Magazine {volume}.{index} - {month:s}/{next_month:s} {year}
```

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

_Calibre Magazine Importer_ imports the magazines as described in the configuration file from the
import directory into Calibre. After a magazine has been imported, it is moved to the archive
directory if one is given for the magazine, else it is deleted from the import directory.

## Changes / History

TODO
