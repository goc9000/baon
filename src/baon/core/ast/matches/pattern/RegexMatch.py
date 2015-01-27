# baon/core/ast/matches/pattern/RegexMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import re

from baon.core.ast.ASTNode import ast_node_field
from baon.core.ast.matches.pattern.ElementaryPatternMatch import ElementaryPatternMatch

from baon.core.ast.rule_check_exceptions import ErrorInRegularExpressionException, InvalidRegexFlagException


class RegexMatch(ElementaryPatternMatch):
    pattern = ast_node_field()
    flags = ast_node_field(hide_for_value=set())

    def __init__(self, pattern, flags=None):
        ElementaryPatternMatch.__init__(self)

        self.pattern = pattern
        self.flags = flags if flags is not None else ()

    def _get_pattern_impl(self):
        # First compile it without the parantheses, as otherwise we would accept malformed expressions such as /)(/
        try:
            re.compile(self.pattern)
        except re.error:
            raise ErrorInRegularExpressionException()

        return '({0})'.format(self.pattern)

    def _get_flags_impl(self):
        flags_enum = re.U
        for flag in self.flags:
            if flag == 'i':
                flags_enum |= re.I
            else:
                raise InvalidRegexFlagException(flag)

        return flags_enum
