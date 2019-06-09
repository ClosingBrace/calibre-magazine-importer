# Calibre Magazine Importer
# A script to import digital magazines into a Calibre library.
#
# Copyright (c) 2019 Hans Vredeveld
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from configparser import ConfigParser
from os.path import expanduser


class MagazineConfiguration(object):
    """The configuration of a single magazine."""

    def __init__(self, magazine, config_section):
        """Initialize the configuration for a single magazine, named by
        magazine, from the config_section. The config_section is a
        section of the ini-file that was read in by
        ImporterConfiguration.
        """
        self._name = magazine
        self._config = config_section


    @property
    def name(self):
        """The magazine's name."""
        return self._name


    @property
    def format(self):
        """The format that the magazine's filename will match."""
        return self._config["format"]


    @property
    def authors(self):
        """The magazine's authors."""
        return self._config["authors"]


    @property
    def languages(self):
        """The languages that the magazine is published in."""
        return self._config.get("languages", raw=True)


    @property
    def publisher(self):
        """The magazine's publisher."""
        return self._config["publisher"]


    @property
    def volume(self):
        """The format for the magazine's volume."""
        return self._config.get("volume", raw=True)


    @property
    def index(self):
        """The format for the magazine's index."""
        return self._config.get("index", raw=True)


    @property
    def year(self):
        """The format for the magazine's year."""
        return self._config.get("year", raw=True)


    @property
    def month(self):
        """The format for the magazine's month."""
        return self._config.get("month", raw=True)


    @property
    def tags(self):
        """The tags that the magazine will be associated with."""
        return self._config.get("tags", raw=True)


    @property
    def title(self):
        """The format for the magazine's title."""
        return self._config["title"]


    @property
    def archivedir(self):
        """The archive directory to which the magazine is moved after
        import.
        """
        return expanduser(self._config.get("archivedir", raw=True))


    def print(self):
        """Print the magazine's configuration."""
        print(f"  Magazine \"{self.name}\"")
        print(f"    format     : {self.format}")
        print(f"    authors    : {self.authors}")
        print(f"    languages  : {self.languages}")
        print(f"    publisher  : {self.publisher}")
        print(f"    volume     : {self.volume}")
        print(f"    index      : {self.index}")
        print(f"    year       : {self.year}")
        print(f"    month      : {self.month}")
        print(f"    tags       : {self.tags}")
        print(f"    title      : {self.title}")
        print(f"    archive dir: {self.archivedir}")
        print()


class ImporterConfiguration(object):
    """The application's configuration. The configuration is read from
    a ini-file. See the README.md for the ini-file's format.
    """

    def __init__(self, config_file):
        """Initialize a configuration object with data from the ini-file
        given by config_file.
        """
        with open(config_file) as f:
            file_content = '[__general__]\n' + f.read()

        self._config = ConfigParser()
        self._config.read_string(file_content)


    @property
    def import_dir(self):
        """Directory from which to import files"""
        return expanduser(self._config["__general__"]["importdir"])


    @property
    def calibredb(self):
        """Path to the calibredb executable"""
        return self._config["__general__"].get("calibredb", "calibredb",
                raw=True)


    @property
    def library_path(self):
        """Path to the calibre library"""
        return expanduser(self._config["__general__"].get("librarypath",
            raw=True))


    @property
    def magazines(self):
        """A list of all the magazines for which import rules have been
        defined."""
        return [mag for mag in self._config.sections() if mag != "__general__"]


    def get_magazine(self, magazine):
        """Get the configuration of the magazine given as argument."""
        return MagazineConfiguration(magazine, self._config[magazine])


    def print(self):
        """Print the configuration."""
        print("Configuration:")
        print("  General settings:")
        print(f"    import dir  : {self.import_dir}")
        print(f"    calibre db  : {self.calibredb}")
        print(f"    library path: {self.library_path}")
        print(f"    magazines   : {self.magazines}")
        print()

        for magazine in self.magazines:
            self.get_magazine(magazine).print()
