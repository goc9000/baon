# baon/core/ast/rules/__tests__/test_Rule.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.core.ast.actions.SaveToAliasAction import SaveToAliasAction
from baon.core.ast.matches.__tests__.MatchTestCase import mark_parens, mark_braces, delete_action
from baon.core.ast.matches.composite.MatchWithActions import MatchWithActions
from baon.core.ast.matches.composite.SequenceMatch import SequenceMatch
from baon.core.ast.matches.immaterial.insertion.InsertAliasMatch import InsertAliasMatch
from baon.core.ast.matches.material.pattern.FormatMatch import FormatMatch
from baon.core.ast.matches.material.pattern.LiteralMatch import LiteralMatch
from baon.core.ast.matches.special.BetweenMatch import BetweenMatch
from baon.core.ast.rules.Rule import Rule


class TestRule(TestCase):

    def test_basic(self):
        self._test_rule(
            text='abc 123',
            rule=Rule(
                SequenceMatch(
                    mark_parens(LiteralMatch('abc')),
                    delete_action(FormatMatch('ws')),
                    mark_braces(FormatMatch('d')),
                ),
            ),
            expected_text='(abc)[123]'
        )

    def test_no_match(self):
        self._test_rule(
            text='abc 123',
            rule=Rule(
                SequenceMatch(
                    mark_parens(LiteralMatch('abc')),
                    delete_action(FormatMatch('ws')),
                    mark_braces(LiteralMatch('x')),
                ),
            ),
            expected_text='abc 123'
        )

    def test_result_includes_text_not_covered_by_matches(self):
        self._test_rule(
            text='abc 123',
            rule=Rule(
                mark_parens(LiteralMatch('ab')),
            ),
            expected_text='(ab)c 123'
        )

    def test_ends_with_between_match(self):
        self._test_rule(
            text='abc 123',
            rule=Rule(
                SequenceMatch(
                    mark_parens(LiteralMatch('ab')),
                    mark_braces(BetweenMatch()),
                ),
            ),
            expected_text='(ab)[c 123]'
        )

    def test_starts_with_between_match(self):
        self._test_rule(
            text='abc 123',
            rule=Rule(
                SequenceMatch(
                    mark_braces(BetweenMatch()),
                    mark_parens(LiteralMatch('c')),
                ),
            ),
            expected_text='[ab](c) 123'
        )

    def test_post_add_alias(self):
        self._test_rule(
            text='abc 123',
            rule=Rule(
                SequenceMatch(
                    LiteralMatch('abc'),
                    MatchWithActions(
                        FormatMatch('d'),
                        SaveToAliasAction('alias'),
                    ),
                    InsertAliasMatch('alias'),
                ),
            ),
            expected_text='abc 123 123',
            expected_aliases={'alias': ' 123'},
        )

    def test_pre_add_alias(self):
        self._test_rule(
            text='abc 123',
            rule=Rule(
                SequenceMatch(
                    InsertAliasMatch('alias'),
                    LiteralMatch('abc'),
                    MatchWithActions(
                        FormatMatch('d'),
                        SaveToAliasAction('alias'),
                    ),
                ),
            ),
            expected_text=' 123abc 123',
            expected_aliases={'alias': ' 123'},
        )

    def _test_rule(self, text, rule, expected_text, aliases=None, expected_aliases=None):
        aliases = aliases or dict()
        expected_aliases = expected_aliases or dict()

        result = rule.apply_on(text, aliases)

        self.assertEqual(result.text, expected_text)
        self.assertEqual(result.aliases, expected_aliases)
