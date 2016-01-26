# baon/core/ast/matches/__tests__/MatchTestCase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

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
