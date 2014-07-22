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
                         ('RULE_SET',))
        self.assertEqual(self.parse_result('rule_set', u';'),
                         ('RULE_SET',))
        self.assertEqual(self.parse_result('rule_set', u'\n'),
                         ('RULE_SET',))
        self.assertEqual(self.parse_result('rule_set', u'  ;  \n ;;\n  \n\n'),
                         ('RULE_SET',))
        self.assertEqual(self.parse_result('rule_set', u'|'),
                         ('RULE_SET',))
        self.assertEqual(self.parse_result('rule_set', u'|;|'),
                         ('RULE_SET',))
        self.assertEqual(self.parse_result('rule_set', u'|||;;||;|;|'),
                         ('RULE_SET',))

    def test_parse_anchor_matches(self):
        self.assertEqual(self.parse_result('match', u'^'),
                         ('START_ANCHOR_MATCH',))
        self.assertEqual(self.parse_result('match', u'$'),
                         ('END_ANCHOR_MATCH',))

    def test_parse_between_match(self):
        self.assertEqual(self.parse_result('match', u'..'),
                         ('BETWEEN_MATCH',))

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

    def test_parse_subrule_match(self):
        self.assertEqual(self.parse_result('match', u'("abc")'),
                         ('SUBRULE_MATCH',
                          ('RULE',
                           ('MATCH_SEQ',
                            ('LITERAL_MATCH', u'abc')))))
        self.assertEqual(self.parse_result('match', u'($|..*)!'),
                         ('SUBRULE_MATCH',
                          ('RULE',
                           ('MATCH_SEQ',
                            ('END_ANCHOR_MATCH',)),
                           ('MATCH_SEQ',
                            ('REPEAT_MATCH',
                             ('BETWEEN_MATCH',),
                             0, None))),
                          ('DELETE_ACTION',)))

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

    def test_parse_apply_rule_set_action(self):
        self.assertEqual(self.parse_result('action', u'->()'),
                         ('RULE_SET_ACTION',
                          ('RULE_SET',)))
        self.assertEqual(self.parse_result('action', u'->(..|%d $\n"abc"!)'),
                         ('RULE_SET_ACTION',
                          ('RULE_SET',
                           ('RULE',
                            ('MATCH_SEQ',
                             ('BETWEEN_MATCH',)),
                            ('MATCH_SEQ',
                             ('FORMAT_MATCH', u'd'),
                             ('END_ANCHOR_MATCH',))),
                           ('RULE',
                            ('MATCH_SEQ',
                             ('LITERAL_MATCH', u'abc',
                              ('DELETE_ACTION',)))))))

    def test_parse_match_with_actions(self):
        self.assertEqual(self.parse_result('match', u'"abc"!'),
                         ('LITERAL_MATCH', u'abc',
                          ('DELETE_ACTION',)))
        self.assertEqual(self.parse_result('match', u'%d>>ghi->"def"'),
                         ('FORMAT_MATCH', u'd',
                          ('SAVE_ACTION', u'ghi'),
                          ('REPLACE_ACTION', u'def')))

    def test_parse_match_with_repeats(self):
        self.assertEqual(self.parse_result('match', u'"abc"?'),
                         ('REPEAT_MATCH', ('LITERAL_MATCH', u'abc'), 0, 1))
        self.assertEqual(self.parse_result('match', u'%d+'),
                         ('REPEAT_MATCH', ('FORMAT_MATCH', u'd'), 1, None))

    def test_parse_match_with_actions_and_repeats(self):
        self.assertEqual(self.parse_result('match', u'"abc"!*'),
                         ('REPEAT_MATCH',
                          ('LITERAL_MATCH', u'abc', ('DELETE_ACTION',)),
                          0, None))
        self.assertEqual(self.parse_result('match', u'"abc"+->"def"'),
                         ('REPEAT_MATCH',
                          ('LITERAL_MATCH', u'abc'),
                          1, None,
                          ('REPLACE_ACTION', u'def')))
        self.assertEqual(self.parse_result('match', u'"abc"+->"def"*!'),
                         ('REPEAT_MATCH',
                          ('REPEAT_MATCH',
                           ('LITERAL_MATCH', u'abc'),
                           1, None,
                           ('REPLACE_ACTION', u'def')),
                          0, None,
                          ('DELETE_ACTION',)))

    def test_parse_search_match(self):
        self.assertEqual(self.parse_result('sequence_match_term', u'@"abc"!'),
                         ('SEARCH_MATCH',
                          ('LITERAL_MATCH', u'abc',
                           ('DELETE_ACTION',))))
        self.assertEqual(self.parse_result('sequence_match_term', u'@..>>etc!'),
                         ('SEARCH_MATCH',
                          ('BETWEEN_MATCH',
                           ('SAVE_ACTION', u'etc'),
                           ('DELETE_ACTION',))))

    def test_parse_match_sequence(self):
        self.assertEqual(self.parse_result('sequence_match', u'.. $'),
                         ('MATCH_SEQ',
                          ('BETWEEN_MATCH',),
                          ('END_ANCHOR_MATCH',)))
        self.assertEqual(self.parse_result('sequence_match', u'^->"abc"..>>def$'),
                         ('MATCH_SEQ',
                          ('START_ANCHOR_MATCH', ('REPLACE_ACTION', u'abc')),
                          ('BETWEEN_MATCH', ('SAVE_ACTION', u'def')),
                          ('END_ANCHOR_MATCH',)))

    def test_parse_rule(self):
        self.assertEqual(self.parse_result('rule', u'..'),
                         ('RULE',
                          ('MATCH_SEQ',
                           ('BETWEEN_MATCH',))))
        self.assertEqual(self.parse_result('rule', u'^|"a"'),
                         ('RULE',
                          ('MATCH_SEQ',
                           ('START_ANCHOR_MATCH',)),
                          ('MATCH_SEQ',
                           ('LITERAL_MATCH', u'a'))))
        self.assertEqual(self.parse_result('rule', u'%d->"a"|..!$|<<abc'),
                         ('RULE',
                          ('MATCH_SEQ',
                           ('FORMAT_MATCH', u'd',
                            ('REPLACE_ACTION', u'a'))),
                          ('MATCH_SEQ',
                           ('BETWEEN_MATCH',
                            ('DELETE_ACTION',)),
                           ('END_ANCHOR_MATCH',)),
                          ('MATCH_SEQ',
                           ('INSERT_ALIAS_MATCH', u'abc'))))

    def test_parse_rule_set(self):
        self.assertEqual(self.parse_result('rule_set', u'..->title;^|"a"!'),
                         ('RULE_SET',
                          ('RULE',
                           ('MATCH_SEQ',
                            ('BETWEEN_MATCH',
                             ('APPLY_FN_ACTION', u'title')))),
                          ('RULE',
                           ('MATCH_SEQ',
                            ('START_ANCHOR_MATCH',)),
                           ('MATCH_SEQ',
                            ('LITERAL_MATCH', u'a',
                             ('DELETE_ACTION',))))))

    def test_syntax_errors(self):
        with self.assertRaisesRegexp(RuleParseException, '(?i)syntax'):
            self.parse_result('rule_set', u'#')
        with self.assertRaisesRegexp(RuleParseException, '(?i)syntax'):
            self.parse_result('rule_set', u'..->#')
        with self.assertRaisesRegexp(RuleParseException, '(?i)syntax'):
            self.parse_result('rule_set', u'..->')
        with self.assertRaisesRegexp(RuleParseException, '(?i)syntax'):
            self.parse_result('rule_set', u'())')

    def parse_result(self, start_rule, rules_text):
        return RulesParser.debug_parse(rules_text, start_rule).test_repr()
