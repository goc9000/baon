# baon/logic/ast/matches/insertion/__tests__/test_AlternativesMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.logic.ast.matches.composite.AlternativesMatch import AlternativesMatch
from baon.logic.ast.matches.pattern.FormatMatch import FormatMatch
from baon.logic.ast.matches.pattern.LiteralMatch import LiteralMatch
from baon.logic.ast.matches.special.EndAnchorMatch import EndAnchorMatch


class TestAlternativesMatch(MatchTestCase):

    def test_alternatives_match(self):
        self._test_match(
            text=u'  123abc',
            match=AlternativesMatch([
                FormatMatch('d'),
                EndAnchorMatch(),
                FormatMatch('ws'),
                LiteralMatch(u'  123abc'),
                LiteralMatch(u'efgh'),
            ]),
            expected_solutions=(
                {'matched_text': u'  123', 'position': 5},
                {'matched_text': u'  ', 'position': 2},
                {'matched_text': u'  123abc', 'position': 8},
            ))
        self._test_no_match(
            text=u'  123abc',
            match=AlternativesMatch())
