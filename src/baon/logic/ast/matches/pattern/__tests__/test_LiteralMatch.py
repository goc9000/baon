# baon/logic/ast/matches/pattern/__tests__/test_LiteralMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.logic.ast.matches.pattern.LiteralMatch import LiteralMatch


class TestLiteralMatch(MatchTestCase):

    def test_basic(self):
        self._test_unique_match(
            text=u'A simple test',
            match=LiteralMatch(u'A simple test'),
            expected_solution={'matched_text': u'A simple test', 'position': 13})

    def test_unicode(self):
        self._test_unique_match(
            text=u"\u00e2\u0103\u00ee\u0219\u021b",
            match=LiteralMatch(u"\u00e2\u0103\u00ee\u0219\u021b"),
            expected_solution={'matched_text': u"\u00e2\u0103\u00ee\u0219\u021b", 'position': 5})

    def test_matches_only_at_start(self):
        self._test_no_match(
            text=u'Must match at start',
            match=LiteralMatch(u'match at start'))

    def test_case_sensitive(self):
        self._test_no_match(
            text=u'Case sensitive',
            match=LiteralMatch(u'CASE SENSITIVE'))

    def test_whitespace_matters(self):
        self._test_no_match(
            text=u'Whitespace matters',
            match=LiteralMatch(u'Whitespace matters '))
