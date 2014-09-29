# baon/logic/ast/actions/__tests__/test_DeleteAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.actions.__tests__.ActionTestCase import ActionTestCase
from baon.logic.ast.actions.DeleteAction import DeleteAction


class TestDeleteAction(ActionTestCase):

    def test_basic(self):
        self._test_simple_text_action(u'Some text', DeleteAction(), u'')

    def test_delete_empty(self):
        self._test_simple_text_action(u'', DeleteAction(), u'')
