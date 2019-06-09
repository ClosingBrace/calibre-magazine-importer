# Calibre Magazine Importer
# A script to import digital magazines into a Calibre library.
#
# Copyright (c) 2019 Hans Vredeveld
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse

from closingbrace.calibre.configuration import ImporterConfiguration
from os.path import expanduser


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

    importer_config.print()
