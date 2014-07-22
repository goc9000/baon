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
                         ('RuleSet',))
        self.assertEqual(self.parse_result('rule_set', u';'),
                         ('RuleSet',))
        self.assertEqual(self.parse_result('rule_set', u'\n'),
                         ('RuleSet',))
        self.assertEqual(self.parse_result('rule_set', u'  ;  \n ;;\n  \n\n'),
                         ('RuleSet',))
        self.assertEqual(self.parse_result('rule_set', u'|'),
                         ('RuleSet',))
        self.assertEqual(self.parse_result('rule_set', u'|;|'),
                         ('RuleSet',))
        self.assertEqual(self.parse_result('rule_set', u'|||;;||;|;|'),
                         ('RuleSet',))

    def test_parse_anchor_matches(self):
        self.assertEqual(self.parse_result('match', u'^'),
                         ('StartAnchorMatch',))
        self.assertEqual(self.parse_result('match', u'$'),
                         ('EndAnchorMatch',))

    def test_parse_between_match(self):
        self.assertEqual(self.parse_result('match', u'..'),
                         ('BetweenMatch',))

    def test_parse_literal_match(self):
        self.assertEqual(self.parse_result('match', u'"abc"'),
                         ('LiteralMatch', u'abc'))
        self.assertEqual(self.parse_result('match', u'"abc'),
                         ('RuleParseException', 'Unterminated string', 1, 1, 1, 4))

    def test_parse_regex_match(self):
        self.assertEqual(self.parse_result('match', u'/abc/'),
                         ('RegexMatch', u'abc'))
        self.assertEqual(self.parse_result('match', u'/abc//def/i'),
                         ('RegexMatch', u'abc/def', {'i'}))
        self.assertEqual(self.parse_result('match', u'/abc'),
                         ('RuleParseException', 'Unterminated regex', 1, 1, 1, 4))

        # Malformed patterns or flags do NOT raise a RuleParseException. This is caught in the semantic check phase.
        self.assertEqual(self.parse_result('match', u'/[abc/'),
                         ('RegexMatch', u'[abc'))
        self.assertEqual(self.parse_result('match', u'/abc/QXYZ'),
                         ('RegexMatch', u'abc', {'Q', 'X', 'Y', 'Z'}))

    def test_parse_format_match(self):
        self.assertEqual(self.parse_result('match', u'%c'),
                         ('FormatMatch', u'c'))
        self.assertEqual(self.parse_result('match', u'%4s'),
                         ('FormatMatch', u's', 4))
        self.assertEqual(self.parse_result('match', u'%04d'),
                         ('FormatMatch', u'd', 4, 'leading'))
        self.assertEqual(self.parse_result('match', u'%'),
                         ('RuleParseException', 'Missing format specifier', 1, 1, 1, 1))

        # Erroneous specifiers do NOT raise a RuleParseException. This is caught in the semantic check phase.
        self.assertEqual(self.parse_result('match', u'%bogus'),
                         ('FormatMatch', u'bogus'))

    def test_parse_insert_alias_match(self):
        self.assertEqual(self.parse_result('match', u'<<abc'),
                         ('InsertAliasMatch', u'abc'))

    def test_parse_insert_literal_match(self):
        self.assertEqual(self.parse_result('match', u'<<"abc"'),
                         ('InsertLiteralMatch', u'abc'))
        self.assertEqual(self.parse_result('match', u'<<"abc'),
                         ('RuleParseException', 'Unterminated string', 1, 3, 1, 6))

    def test_parse_subrule_match(self):
        self.assertEqual(self.parse_result('match', u'("abc")'),
                         ('SubRuleMatch',
                          ('Rule',
                           ('MatchSequence',
                            ('LiteralMatch', u'abc')))))
        self.assertEqual(self.parse_result('match', u'($|..*)!'),
                         ('SubRuleMatch',
                          ('Rule',
                           ('MatchSequence',
                            ('EndAnchorMatch',)),
                           ('MatchSequence',
                            ('RepeatMatch', 0, None,
                             ('BetweenMatch',)))),
                          ('DeleteAction',)))

    def test_parse_delete_action(self):
        self.assertEqual(self.parse_result('action', u'!'),
                         ('DeleteAction',))

    def test_parse_save_to_alias_action(self):
        self.assertEqual(self.parse_result('action', u'>>abc'),
                         ('SaveToAliasAction', u'abc'))

    def test_parse_replace_by_literal_action(self):
        self.assertEqual(self.parse_result('action', u'->"abc"'),
                         ('ReplaceByLiteralAction', u'abc'))
        self.assertEqual(self.parse_result('action', u'->"abc'),
                         ('RuleParseException', 'Unterminated string', 1, 3, 1, 6))

    def test_parse_apply_function_action(self):
        self.assertEqual(self.parse_result('action', u'->title'),
                         ('ApplyFunctionAction', u'title'))

    def test_parse_reformat_action(self):
        self.assertEqual(self.parse_result('action', u'->%c'),
                         ('ReformatAction', u'c'))
        self.assertEqual(self.parse_result('action', u'->%4s'),
                         ('ReformatAction', u's', 4))
        self.assertEqual(self.parse_result('action', u'->%04d'),
                         ('ReformatAction', u'd', 4, 'leading'))
        self.assertEqual(self.parse_result('action', u'->%'),
                         ('RuleParseException', 'Missing format specifier', 1, 3, 1, 3))

        # Erroneous specifiers do NOT raise a RuleParseException. This is caught in the semantic check phase.
        self.assertEqual(self.parse_result('action', u'->%bogus'),
                         ('ReformatAction', u'bogus'))

    def test_parse_apply_rule_set_action(self):
        self.assertEqual(self.parse_result('action', u'->()'),
                         ('ApplyRuleSetAction',
                          ('RuleSet',)))
        self.assertEqual(self.parse_result('action', u'->(..|%d $\n"abc"!)'),
                         ('ApplyRuleSetAction',
                          ('RuleSet',
                           ('Rule',
                            ('MatchSequence',
                             ('BetweenMatch',)),
                            ('MatchSequence',
                             ('FormatMatch', u'd'),
                             ('EndAnchorMatch',))),
                           ('Rule',
                            ('MatchSequence',
                             ('LiteralMatch', u'abc',
                              ('DeleteAction',)))))))

    def test_parse_match_with_actions(self):
        self.assertEqual(self.parse_result('match', u'"abc"!'),
                         ('LiteralMatch', u'abc',
                          ('DeleteAction',)))
        self.assertEqual(self.parse_result('match', u'%d>>ghi->"def"'),
                         ('FormatMatch', u'd',
                          ('SaveToAliasAction', u'ghi'),
                          ('ReplaceByLiteralAction', u'def')))

    def test_parse_match_with_repeats(self):
        self.assertEqual(self.parse_result('match', u'"abc"?'),
                         ('RepeatMatch', 0, 1,
                          ('LiteralMatch', u'abc')))
        self.assertEqual(self.parse_result('match', u'%d+'),
                         ('RepeatMatch', 1, None,
                          ('FormatMatch', u'd')))

    def test_parse_match_with_actions_and_repeats(self):
        self.assertEqual(self.parse_result('match', u'"abc"!*'),
                         ('RepeatMatch', 0, None,
                          ('LiteralMatch', u'abc',
                           ('DeleteAction',))))
        self.assertEqual(self.parse_result('match', u'"abc"+->"def"'),
                         ('RepeatMatch', 1, None,
                          ('LiteralMatch', u'abc'),
                          ('ReplaceByLiteralAction', u'def')))
        self.assertEqual(self.parse_result('match', u'"abc"+->"def"*!'),
                         ('RepeatMatch', 0, None,
                          ('RepeatMatch', 1, None,
                           ('LiteralMatch', u'abc'),
                           ('ReplaceByLiteralAction', u'def')),
                          ('DeleteAction',)))

    def test_parse_search_match(self):
        self.assertEqual(self.parse_result('sequence_match_term', u'@"abc"!'),
                         ('SearchReplaceMatch',
                          ('LiteralMatch', u'abc',
                           ('DeleteAction',))))
        self.assertEqual(self.parse_result('sequence_match_term', u'@..>>etc!'),
                         ('SearchReplaceMatch',
                          ('BetweenMatch',
                           ('SaveToAliasAction', u'etc'),
                           ('DeleteAction',))))

    def test_parse_match_sequence(self):
        self.assertEqual(self.parse_result('sequence_match', u'.. $'),
                         ('MatchSequence',
                          ('BetweenMatch',),
                          ('EndAnchorMatch',)))
        self.assertEqual(self.parse_result('sequence_match', u'^->"abc"..>>def$'),
                         ('MatchSequence',
                          ('StartAnchorMatch',
                           ('ReplaceByLiteralAction', u'abc')),
                          ('BetweenMatch',
                           ('SaveToAliasAction', u'def')),
                          ('EndAnchorMatch',)))

    def test_parse_rule(self):
        self.assertEqual(self.parse_result('rule', u'..'),
                         ('Rule',
                          ('MatchSequence',
                           ('BetweenMatch',))))
        self.assertEqual(self.parse_result('rule', u'^|"a"'),
                         ('Rule',
                          ('MatchSequence',
                           ('StartAnchorMatch',)),
                          ('MatchSequence',
                           ('LiteralMatch', u'a'))))
        self.assertEqual(self.parse_result('rule', u'%d->"a"|..!$|<<abc'),
                         ('Rule',
                          ('MatchSequence',
                           ('FormatMatch', u'd',
                            ('ReplaceByLiteralAction', u'a'))),
                          ('MatchSequence',
                           ('BetweenMatch',
                            ('DeleteAction',)),
                           ('EndAnchorMatch',)),
                          ('MatchSequence',
                           ('InsertAliasMatch', u'abc'))))

    def test_parse_rule_set(self):
        self.assertEqual(self.parse_result('rule_set', u'..->title;^|"a"!'),
                         ('RuleSet',
                          ('Rule',
                           ('MatchSequence',
                            ('BetweenMatch',
                             ('ApplyFunctionAction', u'title')))),
                          ('Rule',
                           ('MatchSequence',
                            ('StartAnchorMatch',)),
                           ('MatchSequence',
                            ('LiteralMatch', u'a',
                             ('DeleteAction',))))))

    def test_syntax_errors(self):
        self.assertEqual(self.parse_result('rule_set', u'#'),
                         ('RuleParseException', 'Syntax error', 1, 1, 1, 1))
        self.assertEqual(self.parse_result('rule_set', u'..->#'),
                         ('RuleParseException', 'Syntax error', 1, 5, 1, 5))
        self.assertEqual(self.parse_result('rule_set', u'..->'),
                         ('RuleParseException', 'Syntax error', 1, 5, 1, 4))
        self.assertEqual(self.parse_result('rule_set', u'())'),
                         ('RuleParseException', 'Syntax error', 1, 3, 1, 3))

    def parse_result(self, start_rule, rules_text):
        try:
            return RulesParser.debug_parse(rules_text, start_rule).test_repr()
        except RuleParseException as e:
            return e.test_repr()
