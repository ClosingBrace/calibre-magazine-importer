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
import re
import shutil
import subprocess

from closingbrace.calibre.configuration import ImporterConfiguration
from closingbrace.calibre.matcher import MagazineMatcher
from os.path import expanduser
from os.path import join


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


def import_magazine(executable, library_path, file_path, magazine):
    """Import a magazine into a Calibre library. The magazine's file
    location is given by file_path, while metadata about the magazine is
    given by magazine.
    The location of the Calibre library is given by library_path, and
    the executable used to import the magazine is given by executable.
    The function returns the book id that the magazine got during
    import.
    When the import failed, a ImportError is raised.
    """
    command = [executable, "add"]
    if library_path is not None:
        command.extend(["--library-path", library_path])
    command.extend(["--authors", magazine.authors,
        "--languages", magazine.languages,
        "--series", magazine.series,
        "--series-index", magazine.number,
        "--tags", magazine.tags,
        "--title", magazine.title,
        file_path])

    exec_result = subprocess.run(command, universal_newlines=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_result = re.match('Added book ids: (\d+)\\n$', exec_result.stdout)

    if not stdout_result or exec_result.stderr:
        raise ImportError(exec_result.stdout, exec_result.stderr)
    return stdout_result[1]


def set_publisher(executable, library_path, book_id, publisher):
    """Set the publisher for an imported book. The location of the
    Calibre library is given by library_path, and the executable used to
    import the magazine is given by executable.
    When setting the publisher failed, a ImportError is raised.
    """
    command = [executable, "set_metadata"]
    if library_path is not None:
        command.extend(["--library-path", library_path])
    command.extend([f"-fpublisher:{publisher}", book_id])

    exec_result = subprocess.run(command, universal_newlines=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if exec_result.returncode != 0:
        raise ImportError(exec_result.stdout, exec_result.stderr)


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
        delete_file = True
        file_path = join(importer_config.import_dir, file)
        matched_magazines = matcher.match(file)
        if not matched_magazines:
            continue

        print(f"File '{file}'")
        for match in matched_magazines:
            try:
                if verbose:
                    match.print()

                book_id = import_magazine(executable=importer_config.calibredb,
                        library_path=importer_config.library_path,
                        file_path=file_path,
                        magazine=match)

                set_publisher(executable=importer_config.calibredb,
                        library_path=importer_config.library_path,
                        book_id=book_id, publisher=match.publisher)
                print("  - successfullly imported into library as '{}'".format(
                    match.title))

                archived_file = join(match.archivedir, match.filename)
                shutil.copy(file_path, archived_file)
                print(f"  - successfullly archived as '{archived_file}'")
            except ImportError as import_error:
                print(f" - NOT imported as '{match.title}'. Error:")
                print(import_error.get_text())
                print()
                delete_file = False
            except OSError as os_error:
                print(f" - NOT archived as '{archived_file}'. Error:")
                print(f"  {os_error}")
                print()
                delete_file = False

        if delete_file:
            os.unlink(file_path)
            print(f"  - successfullly removed from download directory")

        print()
