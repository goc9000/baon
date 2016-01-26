# baon/core/ast/matches/positional/__tests__/test_StartAnchorMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.core.ast.matches.positional.StartAnchorMatch import StartAnchorMatch


class TestStartAnchorMatch(MatchTestCase):

    def test_matches_at_start(self):
        self._test_unique_match(
            text='abc def',
            match=StartAnchorMatch(),
            expected_solution={'matched_text': ''})

    def test_no_match_if_not_at_start(self):
        self._test_no_match(
            text='abc def',
            position=2,
            match=StartAnchorMatch())

    def test_empty(self):
        self._test_unique_match(
            text='',
            match=StartAnchorMatch(),
            expected_solution={'matched_text': ''})
