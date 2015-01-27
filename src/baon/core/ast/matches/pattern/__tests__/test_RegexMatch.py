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
            text='A simple test',
            match=RegexMatch('A simple test'),
            expected_solution={'matched_text': 'A simple test', 'position': 13})
        self._test_unique_match(
            text='Abc  123  def',
            match=RegexMatch('\w+(\s*)[0-9]+'),
            expected_solution={'matched_text': 'Abc  123', 'position': 8})

    def test_case_sensitive(self):
        self._test_unique_match(
            text='CaSE sEnSItivE',
            match=RegexMatch('CaSE sEnSItivE'),
            expected_solution={'matched_text': 'CaSE sEnSItivE', 'position': 14})
        self._test_no_match(
            text='CaSE sEnSItivE',
            match=RegexMatch('CASE SENSITIVE'))
        self._test_unique_match(
            text='CaSE sEnSItivE',
            match=RegexMatch('CASE SENSITIVE', ('i',)),
            expected_solution={'matched_text': 'CaSE sEnSItivE', 'position': 14})

    def test_unicode(self):
        self._test_unique_match(
            text='\u00e2\u0103\u00ee\u0219\u021b',
            match=RegexMatch('\w+'),
            expected_solution={'matched_text': '\u00e2\u0103\u00ee\u0219\u021b', 'position': 5})

    def test_must_match_at_start(self):
        self._test_no_match(
            text='Must match at start',
            match=RegexMatch('match at start'))

    def test_whitespace_matters(self):
        self._test_no_match(
            text='Whitespace matters',
            match=RegexMatch('   Whitespace'))

    def test_anchored(self):
        self._test_unique_match(
            text='Anchored match',
            match=RegexMatch('match'),
            position=9,
            expected_solution={'matched_text': 'match', 'position': 14})
        self._test_no_match(
            text='Anchored match',
            match=RegexMatch('^match'),
            position=9)
        self._test_unique_match(
            text='Anchored match',
            match=RegexMatch('^Anchored'),
            expected_solution={'matched_text': 'Anchored', 'position': 8})
        self._test_no_match(
            text='Anchored match',
            match=RegexMatch('Anchored$'))
        self._test_unique_match(
            text='Anchored match',
            match=RegexMatch('match$'),
            position=9,
            expected_solution={'matched_text': 'match', 'position': 14})
