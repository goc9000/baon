# baon/logic/ast/matches/special/__tests__/test_StartAnchorMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.logic.ast.matches.special.StartAnchorMatch import StartAnchorMatch


class TestStartAnchorMatch(MatchTestCase):

    def test_start_anchor_match(self):
        self._test_unique_match(
            text=u'abc def',
            match=StartAnchorMatch(),
            expected_solution={'matched_text': u''})
        self._test_no_match(
            text=u'abc def',
            position=2,
            match=StartAnchorMatch())
        self._test_unique_match(
            text=u'',
            match=StartAnchorMatch(),
            expected_solution={'matched_text': u''})
