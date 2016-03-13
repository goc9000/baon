# baon/core/ast/matches/special/__tests__/test_SearchReplaceMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.actions.ReplaceByLiteralAction import ReplaceByLiteralAction
from baon.core.ast.actions.SaveToAliasAction import SaveToAliasAction
from baon.core.ast.matches.__tests__.MatchTestCase import MatchTestCase, mark_parens, mark_braces, delete_action
from baon.core.ast.matches.composite.MatchWithActions import MatchWithActions
from baon.core.ast.matches.composite.SequenceMatch import SequenceMatch
from baon.core.ast.matches.pattern.LiteralMatch import LiteralMatch
from baon.core.ast.matches.special.BetweenMatch import BetweenMatch
from baon.core.ast.matches.special.SearchReplaceMatch import SearchReplaceMatch


class TestSearchReplaceMatch(MatchTestCase):

    def test_basic(self):
        self._test_unique_match(
            text='abracadabra',
            match=SearchReplaceMatch(delete_action(LiteralMatch('a'))),
            expected_solution={'text': 'brcdbr', 'matched_text': '', 'position': 0})

    def test_start_in_middle(self):
        self._test_unique_match(
            text='abracadabra',
            match=SearchReplaceMatch(delete_action(LiteralMatch('a'))),
            position=5,
            expected_solution={'text': 'abracdbr', 'matched_text': '', 'position': 5})

    def test_between_match_in_search_at_start(self):
        self._test_unique_match(
            text='abracadabra',
            match=SearchReplaceMatch(
                SequenceMatch(
                    mark_parens(BetweenMatch()),
                    delete_action(LiteralMatch('r')),
                ),
            ),
            expected_solution={'text': '(ab)(acadab)a', 'matched_text': '', 'position': 0})

    def test_between_match_in_search_at_end(self):
        self._test_unique_match(
            text='abracadabra',
            match=SearchReplaceMatch(
                SequenceMatch(
                    delete_action(LiteralMatch('r')),
                    mark_parens(BetweenMatch()),
                ),
            ),
            expected_solution={'text': 'ab(acadab)(a)', 'matched_text': '', 'position': 0})

    def test_between_match_in_search_at_start_and_end(self):
        self._test_unique_match(
            text='abracadabra',
            match=SearchReplaceMatch(
                SequenceMatch(
                    mark_parens(BetweenMatch()),
                    delete_action(LiteralMatch('r')),
                    mark_braces(BetweenMatch()),
                ),
            ),
            expected_solution={'text': '(ab)[acadab]()[a]', 'matched_text': '', 'position': 0})

    def test_recursive_search_replace(self):
        self._test_unique_match(
            text='abracadabra',
            match=SearchReplaceMatch(
                SequenceMatch(
                    delete_action(LiteralMatch('r')),
                    SearchReplaceMatch(
                        MatchWithActions(
                            LiteralMatch('a'),
                            ReplaceByLiteralAction('i'),
                        ),
                    ),
                ),
            ),
            expected_solution={'text': 'abicidibi', 'matched_text': '', 'position': 0})

    def test_captures_aliases(self):
        self._test_unique_match(
            text='abracadabra',
            match=SearchReplaceMatch(
                MatchWithActions(
                    LiteralMatch('r'),
                    SaveToAliasAction('alias'),
                ),
            ),
            expected_solution={'text': 'abracadabra', 'matched_text': '', 'position': 0, 'aliases': {'alias': 'r'}})
