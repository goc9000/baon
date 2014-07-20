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

    def test_parse_insert_alias_match(self):
        self.assertEqual(self.parse_result('match', u'<<abc'),
                         ('INSERT_ALIAS_MATCH', u'abc'))

    def test_parse_insert_literal_match(self):
        self.assertEqual(self.parse_result('match', u'<<"abc"'),
                         ('INSERT_LITERAL_MATCH', u'abc'))
        with self.assertRaisesRegexp(RuleParseException, '(?i)unterminated'):
            self.parse_result('match', u'<<"abc')

    def test_parse_delete_action(self):
        self.assertEqual(self.parse_result('action', u'!'),
                         ('DELETE_ACTION',))

    def test_parse_save_to_alias_action(self):
        self.assertEqual(self.parse_result('action', u'>>abc'),
                         ('SAVE_ACTION', u'abc'))

    def test_parse_replace_by_literal_action(self):
        self.assertEqual(self.parse_result('action', u'->"abc"'),
                         ('REPLACE_ACTION', u'abc'))
        with self.assertRaisesRegexp(RuleParseException, '(?i)unterminated'):
            self.parse_result('action', u'->"abc')

    def test_parse_apply_function_action(self):
        self.assertEqual(self.parse_result('action', u'->title'),
                         ('APPLY_FN_ACTION', u'title'))

    def test_parse_reformat_action(self):
        self.assertEqual(self.parse_result('action', u'->%c'),
                         ('REFORMAT_ACTION', u'c'))
        self.assertEqual(self.parse_result('action', u'->%4s'),
                         ('REFORMAT_ACTION', u's', 4))
        self.assertEqual(self.parse_result('action', u'->%04d'),
                         ('REFORMAT_ACTION', u'd', 4, 'leading'))

        with self.assertRaisesRegexp(RuleParseException, '(?i)missing'):
            self.parse_result('action', u'->%')

        # Erroneous specifiers do NOT raise a RuleParseException. This is caught in the semantic check phase.
        self.assertEqual(self.parse_result('action', u'->%bogus'),
                         ('REFORMAT_ACTION', u'bogus'))

    def test_parse_match_with_actions(self):
        self.assertEqual(self.parse_result('match', u'"abc"!'),
                         ('LITERAL_MATCH', u'abc',
                          ('DELETE_ACTION',)))
        self.assertEqual(self.parse_result('match', u'%d>>ghi->"def"'),
                         ('FORMAT_MATCH', u'd',
                          ('SAVE_ACTION', u'ghi'),
                          ('REPLACE_ACTION', u'def')))

    def parse_result(self, start_rule, rules_text):
        return RulesParser.debug_parse(rules_text, start_rule).test_repr()
