# logic/ast/actions/__tests__/test_actions.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from logic.rules.MatchContext import MatchContext

from logic.ast.actions.DeleteAction import DeleteAction
from logic.ast.actions.ReplaceByLiteralAction import ReplaceByLiteralAction
from logic.ast.actions.SaveToAliasAction import SaveToAliasAction


class TestActions(TestCase):

    def test_delete_action(self):
        self._test_simple_text_action(u'Some text', DeleteAction(), u'')
        self._test_simple_text_action(u'', DeleteAction(), u'')

    def test_replace_by_literal_action(self):
        self._test_simple_text_action(u'Some text', ReplaceByLiteralAction(u'Other text'), u'Other text')
        self._test_simple_text_action(u'', ReplaceByLiteralAction(u'Some text'), u'Some text')
        self._test_simple_text_action(u'', ReplaceByLiteralAction(u''), u'')

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

    def _test_simple_text_action(self, text, action, expected_text):
        test_context = MatchContext(
            text=u'ignored',
            position=0,
            aliases=dict(),
            matched_text=text,
        )

        result_context = action.execute(test_context)

        self.assertEquals(
            result_context,
            test_context._replace(matched_text=expected_text)
        )

    def _test_aliases_action(self, aliases, action, expected_aliases):
        test_context = MatchContext(
            text=u'ignored',
            position=0,
            aliases=aliases,
            matched_text=u'Matched text',
        )

        result_context = action.execute(test_context)

        self.assertEquals(
            result_context,
            test_context._replace(aliases=expected_aliases)
        )
