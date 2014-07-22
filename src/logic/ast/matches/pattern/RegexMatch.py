# logic/ast/matches/pattern/RegexMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import re

from logic.errors.RuleCheckException import RuleCheckException

from logic.ast.RulesASTNode import ast_node_field
from logic.ast.matches.pattern.ElementaryPatternMatch import ElementaryPatternMatch


class RegexMatch(ElementaryPatternMatch):
    pattern = ast_node_field()
    flags = ast_node_field(hide_for_value=set())

    def __init__(self, pattern, flags):
        ElementaryPatternMatch.__init__(self)

        self.pattern = pattern
        self.flags = flags

    def _get_pattern_impl(self):
        return "({0})".format(self.pattern)

    def _get_flags_impl(self):
        flags_enum = 0
        for flag in self.flags:
            if flag == 'i':
                flags_enum |= re.I
            else:
                raise RuleCheckException("Invalid regex flag '{0}'".format(flag))

        return flags_enum
