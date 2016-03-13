# baon/core/ast/matches/composite/__tests__/test_MatchWithActions.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.core.ast.actions.ApplyFunctionAction import ApplyFunctionAction
from baon.core.ast.actions.DeleteAction import DeleteAction
from baon.core.ast.matches.composite.MatchWithActions import MatchWithActions
from baon.core.ast.matches.pattern.LiteralMatch import LiteralMatch


class TestMatchWithActions(MatchTestCase):

    def test_basic(self):
        self._test_unique_match(
            text='abracadabra',
            match=MatchWithActions(
                LiteralMatch('abr'),
                DeleteAction(),
            ),
            expected_solution={'position': 3, 'matched_text': ''})

    def test_no_actions(self):
        self._test_unique_match(
            text='abracadabra',
            match=MatchWithActions(
                LiteralMatch('abr'),
            ),
            expected_solution={'position': 3, 'matched_text': 'abr'})

    def test_chained_actions(self):
        self._test_unique_match(
            text='abracadabra',
            match=MatchWithActions(
                LiteralMatch('abr'),
                ApplyFunctionAction('parens'),
                ApplyFunctionAction('braces'),
                ApplyFunctionAction('curlies'),
            ),
            expected_solution={'position': 3, 'matched_text': '{[(abr)]}'})
