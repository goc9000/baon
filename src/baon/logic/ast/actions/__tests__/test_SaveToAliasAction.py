# baon/logic/ast/actions/__tests__/test_SaveToAliasAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.actions.__tests__.ActionTestCase import ActionTestCase
from baon.logic.ast.actions.SaveToAliasAction import SaveToAliasAction


class TestSaveToAliasAction(ActionTestCase):

    def test_save_to_alias_action(self):
        self._test_aliases_action(
            dict(),
            SaveToAliasAction(u'alias'),
            {u'alias': u'Matched text'}
        )
        self._test_aliases_action(
            {u'alias': u'Previous text'},
            SaveToAliasAction(u'alias'),
            {u'alias': u'Matched text'}
        )
        self._test_aliases_action(
            {u'alias': u'Previous text'},
            SaveToAliasAction(u'new_alias'),
            {u'alias': u'Previous text', u'new_alias': u'Matched text'}
        )
