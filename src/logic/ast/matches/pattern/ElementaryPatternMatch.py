# logic/ast/matches/pattern/ElementaryPatternMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import re

from logic.ast.matches.Match import Match
from logic.errors.RuleCheckException import RuleCheckException


class ElementaryPatternMatch(Match):
    _cached_regex = None

    def __init__(self):
        Match.__init__(self)

    def _get_regex(self):
        if self._cached_regex is not None:
            return self._cached_regex

        pattern = self._get_pattern_impl()
        flags = self._get_flags_impl()

        try:
            self._cached_regex = re.compile(pattern, flags)
            return self._cached_regex
        except re.error:
            raise RuleCheckException('Invalid regex')

    def _get_pattern_impl(self):
        raise RuntimeError('_get_pattern_impl() unimplemented in subclass')

    def _get_flags_impl(self):
        return 0

    def _semanticCheck(self, scope):
        try:
            self._cached_regex = None
            self._get_regex()
        except RuleCheckException as e:
            e.scope = scope
            raise e

    def _execute(self, context):
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
