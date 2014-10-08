# baon/core/ast/matches/pattern/__tests__/test_RegexMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.core.ast.matches.pattern.RegexMatch import RegexMatch


class TestRegexMatch(MatchTestCase):

    def test_basic(self):
        self._test_unique_match(
            text=u'A simple test',
            match=RegexMatch(u'A simple test'),
            expected_solution={'matched_text': u'A simple test', 'position': 13})
        self._test_unique_match(
            text=u'Abc  123  def',
            match=RegexMatch(u'\w+(\s*)[0-9]+'),
            expected_solution={'matched_text': u'Abc  123', 'position': 8})

    def test_case_sensitive(self):
        self._test_unique_match(
            text=u'CaSE sEnSItivE',
            match=RegexMatch(u'CaSE sEnSItivE'),
            expected_solution={'matched_text': u'CaSE sEnSItivE', 'position': 14})
        self._test_no_match(
            text=u'CaSE sEnSItivE',
            match=RegexMatch(u'CASE SENSITIVE'))
        self._test_unique_match(
            text=u'CaSE sEnSItivE',
            match=RegexMatch(u'CASE SENSITIVE', ('i',)),
            expected_solution={'matched_text': u'CaSE sEnSItivE', 'position': 14})

    def test_unicode(self):
        self._test_unique_match(
            text=u'\u00e2\u0103\u00ee\u0219\u021b',
            match=RegexMatch(u'\w+'),
            expected_solution={'matched_text': u'\u00e2\u0103\u00ee\u0219\u021b', 'position': 5})

    def test_must_match_at_start(self):
        self._test_no_match(
            text=u'Must match at start',
            match=RegexMatch(u'match at start'))

    def test_whitespace_matters(self):
        self._test_no_match(
            text=u'Whitespace matters',
            match=RegexMatch(u'   Whitespace'))

    def test_anchored(self):
        self._test_unique_match(
            text=u'Anchored match',
            match=RegexMatch(u'match'),
            position=9,
            expected_solution={'matched_text': u'match', 'position': 14})
        self._test_no_match(
            text=u'Anchored match',
            match=RegexMatch(u'^match'),
            position=9)
        self._test_unique_match(
            text=u'Anchored match',
            match=RegexMatch(u'^Anchored'),
            expected_solution={'matched_text': u'Anchored', 'position': 8})
        self._test_no_match(
            text=u'Anchored match',
            match=RegexMatch(u'Anchored$'))
        self._test_unique_match(
            text=u'Anchored match',
            match=RegexMatch(u'match$'),
            position=9,
            expected_solution={'matched_text': u'match', 'position': 14})
