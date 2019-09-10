# Calibre Magazine Importer
# A script to import digital magazines into a Calibre library.
#
# Copyright (c) 2019 Hans Vredeveld
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from closingbrace.calibre.date_util import Month
from closingbrace.calibre.date_util import to_year
from parse import parse


class MatchedMagazine(object):
    """A magazine that matches a given file."""

    def __init__(self, magazine_config, filename, match_result):
        """Initialize the matched magazine for the given file.
        """
        V = match_result['V'] if 'V' in match_result else 0
        I = match_result['I'] if 'I' in match_result else 0
        Y = to_year(match_result['Y']) if 'Y' in match_result else 0
        M = Month.to_month(match_result['M']) if 'M' in match_result else 0

        eval_globals = {'V': V, 'I': I, 'Y': Y, 'M': M, '__builtins__': {}}

        volume = eval(
                magazine_config.volume, eval_globals
                ) if magazine_config.volume else V
        index = eval(
                magazine_config.index, eval_globals
                ) if magazine_config.index else I
        year = eval(
                magazine_config.year, eval_globals
                ) if magazine_config.year else Y
        month = Month(
                eval(
                    magazine_config.month, eval_globals
                    ) if magazine_config.month else M
                )

        self._filename = filename
        self._series = magazine_config.name
        self._number = f"{volume}.{index:02d}"
        self._authors = magazine_config.authors
        self._languages = magazine_config.languages
        self._publisher = magazine_config.publisher
        self._tags = magazine_config.tags
        self._archivedir = magazine_config.archivedir

        self._title = magazine_config.title.format(
                volume=volume, index=index, year=year,
                month=month, next_month=month.next())


    @property
    def filename(self):
        """The name of the issue's file in the import directory."""
        return self._filename


    @property
    def title(self):
        """The issue's title, including (volume) number and date."""
        return self._title


    @property
    def series(self):
        """The series the magazine belongs to."""
        return self._series


    @property
    def number(self):
        """The magazine's (volume) number, including its index within
        the volume.
        """
        return self._number


    @property
    def authors(self):
        """The magazine's authors."""
        return self._authors


    @property
    def publisher(self):
        """The magazine's publisher."""
        return self._publisher


    @property
    def tags(self):
        """The optional tags associated with the magazine. When there
        are no tags associated with the magazine, this returns None.
        """
        return self._tags


    @property
    def languages(self):
        """The languages the magazine is written in."""
        return self._languages


    @property
    def archivedir(self):
        """The optional directory in which the file is to be archived.
        When this is None, the file will not be archived.
        """
        return self._archivedir


    def print(self):
        """Print the matched magazine."""
        print(f"Match for {self._filename}:")
        print(f"  title            : {self._title}")
        print(f"  series           : {self._series}")
        print(f"  number           : {self._number}")
        print(f"  authors          : {self._authors}")
        print(f"  publisher        : {self._publisher}")
        print(f"  tags             : {self._tags}")
        print(f"  languages        : {self._languages}")
        print(f"  archive directory: {self._archivedir}")
        print()


def create_matched(match_tuple):
    """Create a matched magazine for the given match tuple. The tuple
    contains three elements:
    1. The magazine's configuration.
    2. The file name.
    3. The result of parsing the file name against the magazine's format
       string.
    """
    return MatchedMagazine(match_tuple[0], match_tuple[1], match_tuple[2])


class MagazineMatcher(object):
    """A class to match items against configured magazines."""

    def __init__(self, magazines):
        """Initialize the matcher, giving it the list of magazines to
        match against.
        """
        self._magazines = magazines


    def match(self, file):
        """Match a file name against the list of magazines, returning
        the matching magazines.
        """
        return [create_matched(match) for match in
                ((mag, file, parse(mag.format, file)) for mag in
                    self._magazines)
                if match[2]
                ]
