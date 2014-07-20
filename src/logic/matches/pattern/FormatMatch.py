# logic/matches/pattern/FormatMatch.py
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
    specifier = None
    width = None
    leading_zeros = None

    def __init__(self, specifier, width=None, leading_zeros=False):
        ElementaryPatternMatch.__init__(self)

        self.specifier = specifier
        self.width = width
        self.leading_zeros = leading_zeros

    def _get_pattern_impl(self):
        if self.specifier not in FORMAT_DICT:
            raise RuntimeError("Unrecognized format specifier '{0}'".format(self.specifier))

        pattern, repeat = FORMAT_DICT[self.specifier]

        if self.leading_zeros is not None:
            raise RuntimeError("Leading 0s inapplicable to specifier '{0}'".format(self.specifier))

        if self.width is not None:
            if '##' not in pattern:
                raise RuntimeError("Width inapplicable to specifier '{0}'".format(self.specifier))

            if self.width < 0:
                raise RuntimeError("Invalid width")
            if self.width == 0 and repeat == '+':
                raise  RuntimeError("Width must be at least 1 for specifier '{0}'".format(self.specifier))

            repeat = '{' + str(self.width) + '}'

        return pattern.replace('##', repeat)

    def _test_repr_impl(self):
        base_tuple = 'FORMAT_MATCH', self.specifier

        if self.width is not None:
            base_tuple += self.width,

        if self.leading_zeros is True:
            base_tuple += 'leading',

        return base_tuple
