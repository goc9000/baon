# baon/core/ast/matches/pattern/ElementaryPatternMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import re
from abc import abstractmethod

from baon.core.ast.__errors__.rule_check_errors import ErrorInRegularExpressionError
from baon.core.ast.matches.Match import Match


class ElementaryPatternMatch(Match):
    _cached_regex = None

    def __init__(self):
        Match.__init__(self)

    @abstractmethod
    def _get_pattern_impl(self):
        return ''

    def _get_flags_impl(self):
        return 0

    def _compile_regex(self):
        pattern = self._get_pattern_impl()
        flags = self._get_flags_impl()

        try:
            return re.compile(pattern, flags)
        except re.error:
            raise ErrorInRegularExpressionError() from None

    def _semantic_check_before_children(self, scope):
        self._compile_regex()

    def _get_regex(self):
        if self._cached_regex is not None:
            return self._cached_regex

        self._cached_regex = self._compile_regex()
        return self._cached_regex

    def execute(self, context):
        regex = self._get_regex()

        regex_match = regex.match(context.text, context.position)
        if regex_match is not None:
            yield context._replace(
                position=regex_match.end(0),
                matched_text=regex_match.group(1),
                anchored=True,
            )
