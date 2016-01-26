# baon/core/ast/matches/control/__tests__/test_AlternativesMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.core.ast.matches.control.AlternativesMatch import AlternativesMatch
from baon.core.ast.matches.pattern.FormatMatch import FormatMatch
from baon.core.ast.matches.pattern.LiteralMatch import LiteralMatch
from baon.core.ast.matches.positional.EndAnchorMatch import EndAnchorMatch


class TestAlternativesMatch(MatchTestCase):

    def test_basic(self):
        self._test_match(
            text='  123abc',
            match=AlternativesMatch(
                FormatMatch('d'),
                EndAnchorMatch(),
                FormatMatch('ws'),
                LiteralMatch('  123abc'),
                LiteralMatch('efgh'),
            ),
            expected_solutions=(
                {'matched_text': '  123', 'position': 5},
                {'matched_text': '  ', 'position': 2},
                {'matched_text': '  123abc', 'position': 8},
            ))

    def test_no_alternatives_match(self):
        self._test_no_match(
            text='  123abc',
            match=AlternativesMatch(
                EndAnchorMatch(),
                LiteralMatch('efgh'),
            ))

    def test_no_match_on_empty_alternatives(self):
        self._test_no_match(
            text='  123abc',
            match=AlternativesMatch())
