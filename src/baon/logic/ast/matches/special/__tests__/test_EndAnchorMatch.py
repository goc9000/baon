# baon/logic/ast/matches/special/__tests__/test_EndAnchorMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.logic.ast.matches.special.EndAnchorMatch import EndAnchorMatch


class TestEndAnchorMatch(MatchTestCase):

    def test_end_anchor_match(self):
        self._test_unique_match(
            text=u'abc def',
            match=EndAnchorMatch(),
            position=7,
            expected_solution={'matched_text': u''})
        self._test_no_match(
            text=u'abc def',
            position=2,
            match=EndAnchorMatch())
        self._test_unique_match(
            text=u'',
            match=EndAnchorMatch(),
            expected_solution={'matched_text': u''})
