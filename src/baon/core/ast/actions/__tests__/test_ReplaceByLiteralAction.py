# baon/core/ast/actions/__tests__/test_ReplaceByLiteralAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.actions.__tests__.ActionTestCase import ActionTestCase
from baon.core.ast.actions.ReplaceByLiteralAction import ReplaceByLiteralAction


class TestReplaceByLiteralAction(ActionTestCase):

    def test_basic(self):
        self._test_simple_text_action(u'Some text', ReplaceByLiteralAction(u'Other text'), u'Other text')

    def test_replace_empty(self):
        self._test_simple_text_action(u'', ReplaceByLiteralAction(u'Some text'), u'Some text')

    def test_replace_empty_with_empty(self):
        self._test_simple_text_action(u'', ReplaceByLiteralAction(u''), u'')
