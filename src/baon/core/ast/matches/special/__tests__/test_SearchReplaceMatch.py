# baon/core/ast/matches/special/__tests__/test_SearchReplaceMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.core.ast.actions.DeleteAction import DeleteAction
from baon.core.ast.actions.ApplyFunctionAction import ApplyFunctionAction
from baon.core.ast.actions.ReplaceByLiteralAction import ReplaceByLiteralAction
from baon.core.ast.matches.control.SequenceMatch import SequenceMatch
from baon.core.ast.matches.pattern.LiteralMatch import LiteralMatch
from baon.core.ast.matches.special.SearchReplaceMatch import SearchReplaceMatch
from baon.core.ast.matches.special.BetweenMatch import BetweenMatch


class TestSearchReplaceMatch(MatchTestCase):

    def test_basic(self):
        self._test_unique_match(
            text=u'abracadabra',
            match=SearchReplaceMatch(LiteralMatch(u'a').add_action(DeleteAction())),
            expected_solution={'text': u'brcdbr', 'matched_text': u'', 'position': 0})

    def test_start_in_middle(self):
        self._test_unique_match(
            text=u'abracadabra',
            match=SearchReplaceMatch(LiteralMatch(u'a').add_action(DeleteAction())),
            position=5,
            expected_solution={'text': u'abracdbr', 'matched_text': u'', 'position': 5})

    def test_between_match_in_search_at_start(self):
        self._test_unique_match(
            text=u'abracadabra',
            match=SearchReplaceMatch(
                SequenceMatch(
                    BetweenMatch().add_action(ApplyFunctionAction('paras')),
                    LiteralMatch(u'r').add_action(DeleteAction()),
                )
            ),
            expected_solution={'text': u'(ab)(acadab)a', 'matched_text': u'', 'position': 0})

    def test_between_match_in_search_at_end(self):
        self._test_unique_match(
            text=u'abracadabra',
            match=SearchReplaceMatch(
                SequenceMatch(
                    LiteralMatch(u'r').add_action(DeleteAction()),
                    BetweenMatch().add_action(ApplyFunctionAction('paras')),
                )
            ),
            expected_solution={'text': u'ab(acadab)(a)', 'matched_text': u'', 'position': 0})

    def test_between_match_in_search_at_start_and_end(self):
        self._test_unique_match(
            text=u'abracadabra',
            match=SearchReplaceMatch(
                SequenceMatch(
                    BetweenMatch().add_action(ApplyFunctionAction('paras')),
                    LiteralMatch(u'r').add_action(DeleteAction()),
                    BetweenMatch().add_action(ApplyFunctionAction('braces')),
                )
            ),
            expected_solution={'text': u'(ab)[acadab]()[a]', 'matched_text': u'', 'position': 0})

    def test_recursive_search_replace(self):
        self._test_unique_match(
            text=u'abracadabra',
            match=SearchReplaceMatch(
                SequenceMatch(
                    LiteralMatch(u'r').add_action(DeleteAction()),
                    SearchReplaceMatch(
                        LiteralMatch(u'a').add_action(ReplaceByLiteralAction(u'i'))
                    )
                )
            ),
            expected_solution={'text': u'abicidibi', 'matched_text': u'', 'position': 0})
