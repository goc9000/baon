# logic/parsing/__tests__/test_RulesParser.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from logic.parsing.RulesParser import RulesParser

from logic.errors.RuleParseException import RuleParseException


class TestRulesLexer(TestCase):

    def test_parse_empty(self):
        self.assertEqual(self.parse_result('rule_set', u''),
                         ('RULE_SET', ()))
        self.assertEqual(self.parse_result('rule_set', u';'),
                         ('RULE_SET', ()))
        self.assertEqual(self.parse_result('rule_set', u'\n'),
                         ('RULE_SET', ()))
        self.assertEqual(self.parse_result('rule_set', u'  ;  \n ;;\n  \n\n'),
                         ('RULE_SET', ()))
        self.assertEqual(self.parse_result('rule_set', u'|'),
                         ('RULE_SET', ()))
        self.assertEqual(self.parse_result('rule_set', u'|;|'),
                         ('RULE_SET', ()))
        self.assertEqual(self.parse_result('rule_set', u'|||;;||;|;|'),
                         ('RULE_SET', ()))

    def test_parse_anchor_matches(self):
        self.assertEqual(self.parse_result('match', u'^'),
                         ('START_ANCHOR_MATCH',))
        self.assertEqual(self.parse_result('match', u'$'),
                         ('END_ANCHOR_MATCH',))

    def test_parse_literal_match(self):
        self.assertEqual(self.parse_result('match', u'"abc"'),
                         ('LITERAL_MATCH', u'abc'))
        with self.assertRaisesRegexp(RuleParseException, '(?i)unterminated'):
            self.parse_result('match', u'"abc')

    def test_parse_regex_match(self):
        self.assertEqual(self.parse_result('match', u'/abc/'),
                         ('REGEX_MATCH', u'abc'))
        self.assertEqual(self.parse_result('match', u'/abc//def/i'),
                         ('REGEX_MATCH', u'abc/def', {'i'}))

        with self.assertRaisesRegexp(RuleParseException, '(?i)unterminated'):
            self.parse_result('match', u'/abc')

        # Malformed patterns or flags do NOT raise a RuleParseException. This is caught in the semantic check phase.
        self.assertEqual(self.parse_result('match', u'/[abc/'),
                         ('REGEX_MATCH', u'[abc'))
        self.assertEqual(self.parse_result('match', u'/abc/QXYZ'),
                         ('REGEX_MATCH', u'abc', {'Q', 'X', 'Y', 'Z'}))

    def test_parse_format_match(self):
        self.assertEqual(self.parse_result('match', u'%c'),
                         ('FORMAT_MATCH', u'c'))
        self.assertEqual(self.parse_result('match', u'%4s'),
                         ('FORMAT_MATCH', u's', 4))
        self.assertEqual(self.parse_result('match', u'%04d'),
                         ('FORMAT_MATCH', u'd', 4, 'leading'))

        with self.assertRaisesRegexp(RuleParseException, '(?i)missing'):
            self.parse_result('match', u'%')

        # Erroneous specifiers do NOT raise a RuleParseException. This is caught in the semantic check phase.
        self.assertEqual(self.parse_result('match', u'%bogus'),
                         ('FORMAT_MATCH', u'bogus'))

    def parse_result(self, start_rule, rules_text):
        return RulesParser.debug_parse(rules_text, start_rule).test_repr()
