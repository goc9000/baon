# baon/core/ast/actions/__tests__/test_SaveToAliasAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.actions.__tests__.ActionTestCase import ActionTestCase
from baon.core.ast.actions.SaveToAliasAction import SaveToAliasAction


class TestSaveToAliasAction(ActionTestCase):

    def test_save_first_time(self):
        self._test_aliases_action(
            dict(),
            SaveToAliasAction('alias'),
            {'alias': 'Matched text'}
        )

    def test_save_overwrite(self):
        self._test_aliases_action(
            {'alias': 'Previous text'},
            SaveToAliasAction('alias'),
            {'alias': 'Matched text'}
        )

    def test_preserve_other_aliases(self):
        self._test_aliases_action(
            {'alias': 'Previous text'},
            SaveToAliasAction('new_alias'),
            {'alias': 'Previous text', 'new_alias': 'Matched text'}
        )
