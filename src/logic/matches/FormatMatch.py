# logic/matches/FormatMatch.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import os
import re

from ElementaryPatternMatch import ElementaryPatternMatch

FORMAT_DICT = {
    '%ws':         (r'(\s##)', '*'),
    '%d':          (r'(\s*[0-9]##)', '+'),
    '%c':          (r'(.##)', '{1}'),
    '%s':          (r'(\s*\S##)', '+'),
    '%paras':      (r'(\s*\([^)]##\))', '*'),
    '%inparas':    (r'((?<=\()[^)]##(?=\)))', '*'),
    '%braces':     (r'(\s*\[[^\]]##\])', '*'),
    '%inbraces':   (r'((?<=\[[^\]]##(?=\]))', '*'),
    '%curlies':    (r'(\s*\{[^}]##\})', '*'),
    '%incurlies':  (r'((?<=\{[^}]##(?=\}))', '*'),
    '%path':       (r'(.*' + re.escape(os.sep) + r')', None),
}


class FormatMatch(ElementaryPatternMatch):
    _original_specifier = None
    _original_width = None
    _original_leading = None

    def __init__(self, specifier, width=None, leading_zeros=False):
        ElementaryPatternMatch.__init__(self)

        self._original_specifier = specifier
        self._original_width = width
        self._original_leading = leading_zeros

        try:
            self._setPattern(self._make_pattern(specifier, width, leading_zeros))
        except RuntimeError as e:
            self._setError(e.message)

    def _test_repr_impl(self):
        base_tuple = 'FORMAT_MATCH', self._original_specifier

        if self._original_width is not None:
            base_tuple += self._original_width,

        if self._original_leading is True:
            base_tuple += 'leading',

        return base_tuple

    @staticmethod
    def _make_pattern(specifier, width, leading_zeros):
        if specifier not in FORMAT_DICT:
            raise RuntimeError("Unrecognized format specifier '{0}'".format(specifier))

        pattern, repeat = FORMAT_DICT[specifier]

        if leading_zeros is not None:
            raise RuntimeError("Leading 0s inapplicable to specifier '{0}'".format(specifier))

        if width is not None:
            if '##' not in pattern:
                raise RuntimeError("Width inapplicable to specifier '{0}'".format(specifier))

            if width < 0:
                raise RuntimeError("Invalid width")
            if width == 0 and repeat == '+':
                raise  RuntimeError("Width must be at least 1 for specifier '{0}'".format(specifier))

            repeat = '{' + str(width) + '}'

        return pattern.replace('##', repeat)
