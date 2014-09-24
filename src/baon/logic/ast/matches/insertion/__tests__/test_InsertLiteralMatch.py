# baon/logic/ast/matches/insertion/__tests__/test_InsertLiteralMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.logic.ast.matches.insertion.InsertLiteralMatch import InsertLiteralMatch


class TestInsertLiteralMatch(MatchTestCase):

    def test_insert_literal_match(self):
        self._test_unique_match(
            text=u'abcdef',
            position=3,
            match=InsertLiteralMatch(u'inserted text'),
            expected_solution={'matched_text': u'inserted text'})
        self._test_unique_match(
            text=u'abcdef',
            match=InsertLiteralMatch(u''),
            expected_solution={'matched_text': u''})
