# baon/core/ast/matches/__tests__/MatchTestCase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.core.ast.actions.ApplyFunctionAction import ApplyFunctionAction
from baon.core.ast.actions.DeleteAction import DeleteAction
from baon.core.ast.matches.composite.MatchWithActions import MatchWithActions
from baon.core.rules.MatchContext import MatchContext


class MatchTestCase(TestCase):

    def _test_match(self, text, match, expected_solutions, position=0, aliases=None, anchored=True):

        context = MatchContext(
            text=text,
            position=position,
            aliases=dict() if aliases is None else aliases,
            matched_text=None,
            anchored=anchored,
        )

        expected_solutions = [context._replace(**diff) for diff in expected_solutions]
        solutions = list(match.execute(context))

        self.assertEqual(solutions, expected_solutions)

    def _test_unique_match(self, text, match, expected_solution, **extras):
        self._test_match(text, match, (expected_solution,), **extras)

    def _test_no_match(self, text, match, **extras):
        self._test_match(text, match, (), **extras)


def mark_parens(match):
    """
    Shortcut for decorating a match under test with an "put in parentheses" action
    """
    return MatchWithActions(match, ApplyFunctionAction('parens'))


def mark_braces(match):
    """
    Shortcut for decorating a match under test with an "put in straight braces" action
    """
    return MatchWithActions(match, ApplyFunctionAction('braces'))


def mark_curlies(match):
    """
    Shortcut for decorating a match under test with an "put in curly braces" action
    """
    return MatchWithActions(match, ApplyFunctionAction('curlies'))


def delete_action(match):
    """
    Shortcut for adding a delete action to a match under test
    """
    return MatchWithActions(match, DeleteAction())
