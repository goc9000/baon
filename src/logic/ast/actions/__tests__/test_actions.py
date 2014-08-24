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


class TestActions(TestCase):

    def test_delete_action(self):
        self._test_simple_text_action(u'Some text', DeleteAction(), u'')
        self._test_simple_text_action(u'', DeleteAction(), u'')

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
