# baon/core/ast/actions/__tests__/ActionTestCase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.core.rules.MatchContext import MatchContext


class ActionTestCase(TestCase):

    def _test_simple_text_action(self, text, action, expected_text):
        test_context = MatchContext(
            text=u'ignored',
            position=0,
            aliases=dict(),
            matched_text=text,
            anchored=True,
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
            anchored=True,
        )

        result_context = action.execute(test_context)

        self.assertEquals(
            result_context,
            test_context._replace(aliases=expected_aliases)
        )
