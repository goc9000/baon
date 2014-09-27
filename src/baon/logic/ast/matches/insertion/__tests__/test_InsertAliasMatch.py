# baon/logic/ast/matches/insertion/__tests__/test_InsertAliasMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.logic.ast.matches.insertion.InsertAliasMatch import InsertAliasMatch


class TestInsertAliasMatch(MatchTestCase):

    def test_existing_alias(self):
        self._test_unique_match(
            text=u'abcdef',
            position=3,
            aliases={u'alias1': u'content1', u'alias2': u'content2'},
            match=InsertAliasMatch(u'alias1'),
            expected_solution={'matched_text': u'content1'})

    def test_nonexisting_alias(self):
        self._test_unique_match(
            text=u'abcdef',
            position=3,
            aliases={u'alias1': u'content1', u'alias2': u'content2'},
            match=InsertAliasMatch(u'non_existent'),
            expected_solution={'matched_text': u''})
