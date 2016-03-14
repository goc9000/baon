# baon/core/ast/actions/__tests__/ActionTestCase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.core.rules.ActionContext import ActionContext


class ActionTestCase(TestCase):

    def _test_simple_text_action(self, text, action, expected_text):
        test_context = ActionContext(text=text, aliases=dict())

        result_context = action.execute(test_context)

        self.assertEquals(
            result_context,
            test_context._replace(text=expected_text)
        )

    def _test_aliases_action(self, aliases, action, expected_aliases):
        test_context = ActionContext(text='Matched text', aliases=aliases)

        result_context = action.execute(test_context)

        self.assertEquals(
            result_context,
            test_context._replace(aliases=expected_aliases)
        )
