# baon/logic/ast/matches/special/__tests__/test_BetweenMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.logic.ast.matches.pattern.LiteralMatch import LiteralMatch
from baon.logic.ast.matches.special.BetweenMatch import BetweenMatch

from baon.logic.rules.MatchContext import MatchContext


class TestBetweenMatch(MatchTestCase):

    def test_basic(self):
        self._test_match(
            text=u'abc d',
            match=BetweenMatch(),
            expected_solutions=[
                {'matched_text': u'', 'position': 0, 'anchored': False},
                {'matched_text': u'a', 'position': 1, 'anchored': False},
                {'matched_text': u'ab', 'position': 2, 'anchored': False},
                {'matched_text': u'abc', 'position': 3, 'anchored': False},
                {'matched_text': u'abc ', 'position': 4, 'anchored': False},
                {'matched_text': u'abc d', 'position': 5, 'anchored': False},
            ])

    def test_between_match_is_empty_if_unanchored(self):
        self._test_unique_match(
            text=u'abc d',
            match=BetweenMatch(),
            anchored=False,
            expected_solution={'matched_text': u'', 'position': 0})
