# Calibre Magazine Importer
# A script to import digital magazines into a Calibre library.
#
# Copyright (c) 2019 Hans Vredeveld
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import os

from closingbrace.calibre.configuration import ImporterConfiguration
from closingbrace.calibre.matcher import MagazineMatcher
from os.path import expanduser


class ImportError(Exception):
    """Exception raised when something went wrong during the import of
    a magazine.
    """

    def __init__(self, stdout_text, stderr_text):
        """Initialize the exception, using the text that was output to
        stdout and stderr to create an error text.
        """
        self._error_text = (f"  stdout: {stdout_text}\n  stderr: {stderr_text}")


    def get_text(self):
        """Get the error text from the exception."""
        return self._error_text


def parse_command_line():
    """Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
            description="Import magazines into Calibre")
    parser.add_argument("-c", "--config",
            default=expanduser("~/.calibre-magazine-importer"),
            help="configuration file for the importer (default: "
            "$HOME/.calibre-magazine-importer)")
    parser.add_argument("-v", "--verbose", help="be more verbose about "
            "the magazines that are imported", action="store_true")
    return parser.parse_args()


def run():
    """Run the importer application."""
    cmd_line = parse_command_line()
    importer_config = ImporterConfiguration(cmd_line.config)
    verbose = cmd_line.verbose

    if verbose:
        importer_config.print()
        print(f"Processing files in directory {importer_config.import_dir}")
        print()

    matcher = MagazineMatcher(
            [importer_config.get_magazine(mag_name)
                for mag_name in importer_config.magazines]
            )
    files = next(os.walk(importer_config.import_dir))[2]
    for file in files:
        matched_magazines = matcher.match(file)

        for match in matched_magazines:
            if verbose:
                match.print()
