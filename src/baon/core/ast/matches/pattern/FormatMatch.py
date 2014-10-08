# baon/core/ast/matches/pattern/FormatMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os
import re

from baon.core.errors.RuleCheckException import RuleCheckException

from baon.core.ast.matches.pattern.ElementaryPatternMatch import ElementaryPatternMatch
from baon.core.ast.ASTNode import ast_node_field


FORMAT_DICT = {
    'ws':         (r'(\s##)', '*'),
    'd':          (r'(\s*[0-9]##)', '+'),
    'c':          (r'(.##)', '{1}'),
    's':          (r'(\s*\S##)', '+'),
    'paras':      (r'(\s*\([^)]##\))', '*'),
    'braces':     (r'(\s*\[[^\]]##\])', '*'),
    'curlies':    (r'(\s*\{[^}]##\})', '*'),
    'inparas':    (r'((?<=\()[^)]##(?=\)))', '*'),
    'inbraces':   (r'((?<=\[)[^\]]##(?=\]))', '*'),
    'incurlies':  (r'((?<=\{)[^}]##(?=\}))', '*'),
    'path':       (r'(.*' + re.escape(os.sep) + r')', None),
}


class FormatMatch(ElementaryPatternMatch):
    specifier = ast_node_field()
    width = ast_node_field()
    leading_zeros = ast_node_field(test_repr='leading')

    def __init__(self, specifier, width=None, leading_zeros=False):
        ElementaryPatternMatch.__init__(self)

        self.specifier = specifier
        self.width = width
        self.leading_zeros = leading_zeros

    def _get_pattern_impl(self):
        if self.specifier not in FORMAT_DICT:
            raise RuleCheckException("Unrecognized format specifier '{0}'".format(self.specifier))

        pattern, repeat = FORMAT_DICT[self.specifier]

        if self.leading_zeros is True:
            raise RuleCheckException("Leading 0s inapplicable to specifier '{0}'".format(self.specifier))

        if self.width is not None:
            if '##' not in pattern:
                raise RuleCheckException("Width inapplicable to specifier '{0}'".format(self.specifier))

            if self.width < 0:
                raise RuleCheckException("Invalid width")
            if self.width == 0 and repeat in ['+', '{1}']:
                raise RuleCheckException("Width must be at least 1 for specifier '{0}'".format(self.specifier))

            repeat = '{' + str(self.width) + '}'

        if repeat is not None:
            pattern = pattern.replace(u'##', repeat)

        return pattern
