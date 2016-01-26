# baon/core/ast/matches/insertion/__tests__/test_InsertAliasMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.__tests__.MatchTestCase import MatchTestCase
from baon.core.ast.matches.insertion.InsertAliasMatch import InsertAliasMatch


class TestInsertAliasMatch(MatchTestCase):

    def test_existing_alias(self):
        self._test_unique_match(
            text='abcdef',
            position=3,
            aliases={'alias1': 'content1', 'alias2': 'content2'},
            match=InsertAliasMatch('alias1'),
            expected_solution={'matched_text': 'content1'})

    def test_nonexisting_alias(self):
        self._test_unique_match(
            text='abcdef',
            position=3,
            aliases={'alias1': 'content1', 'alias2': 'content2'},
            match=InsertAliasMatch('non_existent'),
            expected_solution={'matched_text': ''})
