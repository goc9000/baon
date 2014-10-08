# baon/core/ast/matches/insertion/__tests__/test_InsertLiteralMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.core.ast.matches.insertion.InsertLiteralMatch import InsertLiteralMatch


class TestInsertLiteralMatch(MatchTestCase):

    def test_basic(self):
        self._test_unique_match(
            text=u'abcdef',
            position=3,
            match=InsertLiteralMatch(u'inserted text'),
            expected_solution={'matched_text': u'inserted text'})

    def test_insert_empty(self):
        self._test_unique_match(
            text=u'abcdef',
            match=InsertLiteralMatch(u''),
            expected_solution={'matched_text': u''})
