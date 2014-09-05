# baon/logic/ast/matches/pattern/ElementaryPatternMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import re

from baon.logic.ast.matches.MatchWithActions import MatchWithActions
from baon.logic.errors.RuleCheckException import RuleCheckException


class ElementaryPatternMatch(MatchWithActions):
    _cached_regex = None

    def __init__(self):
        MatchWithActions.__init__(self)

    def _get_pattern_impl(self):
        raise RuntimeError('_get_pattern_impl() unimplemented in subclass')

    def _get_flags_impl(self):
        return 0

    def _compile_regex(self):
        pattern = self._get_pattern_impl()
        flags = self._get_flags_impl()

        try:
            return re.compile(pattern, flags)
        except re.error:
            raise RuleCheckException('Error in regular expression')

    def _semantic_check_before_children(self, scope):
        self._compile_regex()

    def _get_regex(self):
        if self._cached_regex is not None:
            return self._cached_regex

        self._cached_regex = self._compile_regex()
        return self._cached_regex

    def _execute_match_with_actions_impl(self, context):
        regex = self._get_regex()

        if context.next_unanchored:
            m = regex.search(context.text, context.position)
            context.next_unanchored = False
        else:
            m = regex.match(context.text, context.position)

        if m is None:
            return False

        context.position = m.end(0)
        context.last_match_pos = m.start(1)

        return m.group(1)