# baon/core/parsing/__tests__/test_parse_rules.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.core.parsing.__errors__.rule_parse_errors import RuleParseError

from baon.core.parsing.parse_rules import parse_rules


class TestRulesLexer(TestCase):

    def test_parse_empty(self):
        self.assertEqual(self.parse_result('rule_set', ''),
                         ('RuleSet',))
        self.assertEqual(self.parse_result('rule_set', ';'),
                         ('RuleSet',))
        self.assertEqual(self.parse_result('rule_set', '\n'),
                         ('RuleSet',))
        self.assertEqual(self.parse_result('rule_set', '  ;  \n ;;\n  \n\n'),
                         ('RuleSet',))
        self.assertEqual(self.parse_result('rule_set', '|'),
                         ('RuleSet',))
        self.assertEqual(self.parse_result('rule_set', '|;|'),
                         ('RuleSet',))
        self.assertEqual(self.parse_result('rule_set', '|||;;||;|;|'),
                         ('RuleSet',))

    def test_parse_anchor_matches(self):
        self.assertEqual(self.parse_result('match', '^'),
                         ('StartAnchorMatch',))
        self.assertEqual(self.parse_result('match', '$'),
                         ('EndAnchorMatch',))

    def test_parse_between_match(self):
        self.assertEqual(self.parse_result('match', '..'),
                         ('BetweenMatch',))

    def test_parse_literal_match(self):
        self.assertEqual(self.parse_result('match', '"abc"'),
                         ('LiteralMatch', 'abc'))
        self.assertEqual(self.parse_result('match', '"abc'),
                         ('UnterminatedStringError', 1, 1, 1, 4))

    def test_parse_regex_match(self):
        self.assertEqual(self.parse_result('match', '/abc/'),
                         ('RegexMatch', 'abc'))
        self.assertEqual(self.parse_result('match', '/abc//def/i'),
                         ('RegexMatch', 'abc/def', {'i'}))
        self.assertEqual(self.parse_result('match', '/abc'),
                         ('UnterminatedRegexError', 1, 1, 1, 4))

        # Malformed patterns or flags do NOT raise a RuleParseException. This is caught in the semantic check phase.
        self.assertEqual(self.parse_result('match', '/[abc/'),
                         ('RegexMatch', '[abc'))
        self.assertEqual(self.parse_result('match', '/abc/QXYZ'),
                         ('RegexMatch', 'abc', {'Q', 'X', 'Y', 'Z'}))

    def test_parse_format_match(self):
        self.assertEqual(self.parse_result('match', '%c'),
                         ('FormatMatch', 'c'))
        self.assertEqual(self.parse_result('match', '%4s'),
                         ('FormatMatch', 's', 4))
        self.assertEqual(self.parse_result('match', '%04d'),
                         ('FormatMatch', 'd', 4, 'leading'))
        self.assertEqual(self.parse_result('match', '%'),
                         ('MissingFormatSpecifierError', 1, 1, 1, 1))

        # Erroneous specifiers do NOT raise a RuleParseError. This is caught in the semantic check phase.
        self.assertEqual(self.parse_result('match', '%bogus'),
                         ('FormatMatch', 'bogus'))

    def test_parse_insert_alias_match(self):
        self.assertEqual(self.parse_result('match', '<<abc'),
                         ('InsertAliasMatch', 'abc'))

    def test_parse_insert_literal_match(self):
        self.assertEqual(self.parse_result('match', '<<"abc"'),
                         ('InsertLiteralMatch', 'abc'))
        self.assertEqual(self.parse_result('match', '<<"abc'),
                         ('UnterminatedStringError', 1, 3, 1, 6))

    def test_parse_subrule_match(self):
        self.assertEqual(self.parse_result('match', '("abc")'),
                         ('AlternativesMatch',
                          ('SequenceMatch',
                           ('LiteralMatch', 'abc'))))
        self.assertEqual(self.parse_result('match', '($|..*)!'),
                         ('AlternativesMatch',
                          ('SequenceMatch',
                           ('EndAnchorMatch',)),
                          ('SequenceMatch',
                           ('RepeatMatch', 0, None,
                            ('BetweenMatch',))),
                          ('DeleteAction',)))

    def test_parse_delete_action(self):
        self.assertEqual(self.parse_result('action', '!'),
                         ('DeleteAction',))

    def test_parse_save_to_alias_action(self):
        self.assertEqual(self.parse_result('action', '>>abc'),
                         ('SaveToAliasAction', 'abc'))

    def test_parse_replace_by_literal_action(self):
        self.assertEqual(self.parse_result('action', '->"abc"'),
                         ('ReplaceByLiteralAction', 'abc'))
        self.assertEqual(self.parse_result('action', '->"abc'),
                         ('UnterminatedStringError', 1, 3, 1, 6))

    def test_parse_apply_function_action(self):
        self.assertEqual(self.parse_result('action', '->title'),
                         ('ApplyFunctionAction', 'title'))

    def test_parse_reformat_action(self):
        self.assertEqual(self.parse_result('action', '->%c'),
                         ('ReformatAction', 'c'))
        self.assertEqual(self.parse_result('action', '->%4s'),
                         ('ReformatAction', 's', 4))
        self.assertEqual(self.parse_result('action', '->%04d'),
                         ('ReformatAction', 'd', 4, 'leading'))
        self.assertEqual(self.parse_result('action', '->%'),
                         ('MissingFormatSpecifierError', 1, 3, 1, 3))

        # Erroneous specifiers do NOT raise a RuleParseError. This is caught in the semantic check phase.
        self.assertEqual(self.parse_result('action', '->%bogus'),
                         ('ReformatAction', 'bogus'))

    def test_parse_apply_rule_set_action(self):
        self.assertEqual(self.parse_result('action', '->()'),
                         ('ApplyRuleSetAction',
                          ('RuleSet',)))
        self.assertEqual(self.parse_result('action', '->(..|%d $\n"abc"!)'),
                         ('ApplyRuleSetAction',
                          ('RuleSet',
                           ('Rule',
                            ('AlternativesMatch',
                             ('SequenceMatch',
                              ('BetweenMatch',)),
                             ('SequenceMatch',
                              ('FormatMatch', 'd'),
                              ('EndAnchorMatch',)))),
                           ('Rule',
                            ('AlternativesMatch',
                             ('SequenceMatch',
                              ('LiteralMatch', 'abc',
                               ('DeleteAction',))))))))

    def test_parse_match_with_actions(self):
        self.assertEqual(self.parse_result('match', '"abc"!'),
                         ('LiteralMatch', 'abc',
                          ('DeleteAction',)))
        self.assertEqual(self.parse_result('match', '%d>>ghi->"def"'),
                         ('FormatMatch', 'd',
                          ('SaveToAliasAction', 'ghi'),
                          ('ReplaceByLiteralAction', 'def')))

    def test_parse_match_with_repeats(self):
        self.assertEqual(self.parse_result('match', '"abc"?'),
                         ('RepeatMatch', 0, 1,
                          ('LiteralMatch', 'abc')))
        self.assertEqual(self.parse_result('match', '%d+'),
                         ('RepeatMatch', 1, None,
                          ('FormatMatch', 'd')))

    def test_parse_match_with_actions_and_repeats(self):
        self.assertEqual(self.parse_result('match', '"abc"!*'),
                         ('RepeatMatch', 0, None,
                          ('LiteralMatch', 'abc',
                           ('DeleteAction',))))
        self.assertEqual(self.parse_result('match', '"abc"+->"def"'),
                         ('RepeatMatch', 1, None,
                          ('LiteralMatch', 'abc'),
                          ('ReplaceByLiteralAction', 'def')))
        self.assertEqual(self.parse_result('match', '"abc"+->"def"*!'),
                         ('RepeatMatch', 0, None,
                          ('RepeatMatch', 1, None,
                           ('LiteralMatch', 'abc'),
                           ('ReplaceByLiteralAction', 'def')),
                          ('DeleteAction',)))

    def test_parse_search_match(self):
        self.assertEqual(self.parse_result('sequence_match_term', '@"abc"!'),
                         ('SearchReplaceMatch',
                          ('LiteralMatch', 'abc',
                           ('DeleteAction',))))
        self.assertEqual(self.parse_result('sequence_match_term', '@..>>etc!'),
                         ('SearchReplaceMatch',
                          ('BetweenMatch',
                           ('SaveToAliasAction', 'etc'),
                           ('DeleteAction',))))

    def test_parse_sequence_match(self):
        self.assertEqual(self.parse_result('sequence_match', '.. $'),
                         ('SequenceMatch',
                          ('BetweenMatch',),
                          ('EndAnchorMatch',)))
        self.assertEqual(self.parse_result('sequence_match', '^->"abc"..>>def$'),
                         ('SequenceMatch',
                          ('StartAnchorMatch',
                           ('ReplaceByLiteralAction', 'abc')),
                          ('BetweenMatch',
                           ('SaveToAliasAction', 'def')),
                          ('EndAnchorMatch',)))

    def test_parse_rule(self):
        self.assertEqual(self.parse_result('rule', '..'),
                         ('Rule',
                          ('AlternativesMatch',
                           ('SequenceMatch',
                            ('BetweenMatch',)))))
        self.assertEqual(self.parse_result('rule', '^|"a"'),
                         ('Rule',
                          ('AlternativesMatch',
                           ('SequenceMatch',
                            ('StartAnchorMatch',)),
                           ('SequenceMatch',
                            ('LiteralMatch', 'a')))))
        self.assertEqual(self.parse_result('rule', '%d->"a"|..!$|<<abc'),
                         ('Rule',
                          ('AlternativesMatch',
                           ('SequenceMatch',
                            ('FormatMatch', 'd',
                             ('ReplaceByLiteralAction', 'a'))),
                           ('SequenceMatch',
                            ('BetweenMatch',
                             ('DeleteAction',)),
                            ('EndAnchorMatch',)),
                           ('SequenceMatch',
                            ('InsertAliasMatch', 'abc')))))

    def test_parse_rule_set(self):
        self.assertEqual(self.parse_result('rule_set', '..->title;^|"a"!'),
                         ('RuleSet',
                          ('Rule',
                           ('AlternativesMatch',
                            ('SequenceMatch',
                             ('BetweenMatch',
                              ('ApplyFunctionAction', 'title'))))),
                          ('Rule',
                           ('AlternativesMatch',
                            ('SequenceMatch',
                             ('StartAnchorMatch',)),
                            ('SequenceMatch',
                             ('LiteralMatch', 'a',
                              ('DeleteAction',)))))))

    def test_syntax_errors(self):
        self.assertEqual(self.parse_result('rule_set', '#'),
                         ('RuleSyntaxError', 1, 1, 1, 1))
        self.assertEqual(self.parse_result('rule_set', '..->#'),
                         ('RuleSyntaxError', 1, 5, 1, 5))
        self.assertEqual(self.parse_result('rule_set', '..->'),
                         ('RuleSyntaxError', 1, 5, 1, 4))
        self.assertEqual(self.parse_result('rule_set', '())'),
                         ('RuleSyntaxError', 1, 3, 1, 3))

    def parse_result(self, start_rule, rules_text):
        try:
            return parse_rules(rules_text, start_rule).test_repr()
        except RuleParseError as e:
            return e.test_repr()
