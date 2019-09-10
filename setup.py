# Calibre Magazine Importer
# A script to import digital magazines into a Calibre library.
#
# Copyright (c) 2019 Hans Vredeveld
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='closingbrace_calibre_magazine_importer',
    version='0.1.0',
    description='A script to import digital magazines into a Calibre library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/closingbrace/calibre-magazine-importer",
    author='Hans Vredeveld',
    author_email='github@closingbrace.nl',
    license='Mozilla Public License 2.0',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    packages=['closingbrace.calibre'],
    python_requires='~=3.3',
    install_requires=['parse==1.12.0'],
    entry_points={
        'console_scripts': [
            'calibre-magazine-importer=closingbrace.calibre.importer:run',
        ],
    },
    zip_safe=False,
)
