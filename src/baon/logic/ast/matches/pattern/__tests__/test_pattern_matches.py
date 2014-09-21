# baon/logic/ast/matches/pattern/__tests__/test_pattern_matches.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.logic.ast.matches.pattern.LiteralMatch import LiteralMatch


class TestPatternMatches(MatchTestCase):

    def test_literal_match(self):
        self._test_unique_match(
            text=u'A simple test',
            match=LiteralMatch(u'A simple test'),
            expected_solution={'matched_text': u'A simple test', 'position': 13})
        self._test_unique_match(
            text=u"\u00e2\u0103\u00ee\u0219\u021b Unicode also works",
            match=LiteralMatch(u"\u00e2\u0103\u00ee\u0219\u021b"),
            expected_solution={'matched_text': u"\u00e2\u0103\u00ee\u0219\u021b", 'position': 5})
        self._test_no_match(
            text=u'Must match at start',
            match=LiteralMatch(u'match at start'))
        self._test_no_match(
            text=u'Case sensitive',
            match=LiteralMatch(u'CASE SENSITIVE'))
        self._test_no_match(
            text=u'Whitespace matters',
            match=LiteralMatch(u'Whitespace matters '))
