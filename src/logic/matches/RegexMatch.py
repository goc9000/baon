# logic/matches/RegexMatch.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import re

from ElementaryPatternMatch import ElementaryPatternMatch


class RegexMatch(ElementaryPatternMatch):
    _original_pattern = None
    _original_flags = None

    def __init__(self, pattern, flags):
        ElementaryPatternMatch.__init__(self)

        self._original_pattern = pattern
        self._original_flags = flags

        flags_enum = 0
        for c in flags:
            if c == 'i':
                flags_enum |= re.I
            else:
                self._setError("Invalid regex flag '{0}'".format(c))
                return

        self._setPattern("({0})".format(pattern), flags_enum)

    def _test_repr_impl(self):
        base_tuple = 'REGEX_MATCH', self._original_pattern

        if len(self._original_flags) > 0:
            base_tuple += self._original_flags,

        return base_tuple
