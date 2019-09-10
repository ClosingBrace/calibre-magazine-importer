# Calibre Magazine Importer
# A script to import digital magazines into a Calibre library.
#
# Copyright (c) 2019 Hans Vredeveld
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

class Month(object):
    """A month of the year."""

    def __init__(self, number):
        """Create a month instance for the month given by number. The
        number must be in the range 0 to 12 inclusive. Here, 0 denotes
        an unspecified month, and the other values the usual month
        numbers.
        """
        self._month = number


    def __format__(self, format_spec):
        """Format the month acording to the format specification. In the
        format specification, the specifiers for integers and strings
        can be used. When a format specifier for integers is used, the
        month is out as a number and when the format specifier for a
        string is used, the month is output as a string. When no format
        specifier is given, the month is output as an integer.
        """
        if format_spec[-1:] == 's':
            month_names = ['',
                    'January', 'February', 'March', 'April',
                    'May', 'June', 'July', 'August',
                    'September', 'October', 'November', 'December'
                    ]
            return f"{month_names[self._month]:{format_spec}}"
        return f"{self._month:{format_spec}}"


    def next(self):
        """Return the month following this month. If the month is 12
        (December), it will return 1 (January) without adjusting the
        year. If the month is unspecified (its value is 0), the month
        returned is also unspecified.
        """
        if self._month == 0:
            return Month(0)
        if self._month == 12:
            return Month(1)
        return Month(self._month + 1)


    @staticmethod
    def to_month(month_id):
        """Convert a string representation for a month to the month as a
        number between 1 and 12 (inclusive). The string representation
        can be a one or two character string with the month as a number,
        or it can be a string of at least three characters with the case
        insensitive (abreviated) month name. The function is locale
        independent and only supports names in English.
        """
        months = {
                '1': 1, '01': 1, 'jan': 1,
                '2': 2, '02': 2, 'feb': 2,
                '3': 3, '03': 3, 'mar': 3,
                '4': 4, '04': 4, 'apr': 4,
                '5': 5, '05': 5, 'may': 5,
                '6': 6, '06': 6, 'jun': 6,
                '7': 7, '07': 7, 'jul': 7,
                '8': 8, '08': 8, 'aug': 8,
                '9': 9, '09': 9, 'sep': 9,
                '10': 10, 'oct': 10,
                '11': 11, 'nov': 11,
                '12': 12, 'dec': 12
                }
        return months[month_id[:3].lower()]
