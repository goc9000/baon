# baon/logic/ast/actions/__tests__/test_ReformatAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.actions.__tests__.ActionTestCase import ActionTestCase
from baon.logic.ast.actions.ReformatAction import ReformatAction

from baon.logic.errors.RuleApplicationException import RuleApplicationException


class TestReformatAction(ActionTestCase):

    def test_reformat_action(self):
        self._test_simple_text_action(u'123', ReformatAction('d'), u'123')
        self._test_simple_text_action(u'0045', ReformatAction('d'), u'45')
        self._test_simple_text_action(u'  78 ', ReformatAction('d'), u'  78 ')

        self._test_simple_text_action(u'1234', ReformatAction('d', 3), u'1234')
        self._test_simple_text_action(u'0045', ReformatAction('d', 3), u'045')
        self._test_simple_text_action(u'  78 ', ReformatAction('d', 3), u'  078 ')

        with self.assertRaisesRegexp(RuleApplicationException, 'non-number'):
            self._test_simple_text_action(u'00abc', ReformatAction('d'), u'should fail')
