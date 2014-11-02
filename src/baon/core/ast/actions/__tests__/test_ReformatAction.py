# baon/core/ast/actions/__tests__/test_ReformatAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.actions.__tests__.ActionTestCase import ActionTestCase
from baon.core.ast.actions.ReformatAction import ReformatAction

from baon.core.ast.rule_application_exceptions import SpecifierExpectsNumberException


class TestReformatAction(ActionTestCase):

    def test_d_basic(self):
        self._test_simple_text_action(u'123', ReformatAction('d'), u'123')
        self._test_simple_text_action(u'0045', ReformatAction('d'), u'45')

    def test_d_shorter_length(self):
        self._test_simple_text_action(u'1234', ReformatAction('d', 3), u'1234')
        self._test_simple_text_action(u'0045', ReformatAction('d', 3), u'045')

    def test_d_longer_length(self):
        self._test_simple_text_action(u'1234', ReformatAction('d', 5), u'01234')
        self._test_simple_text_action(u'0045', ReformatAction('d', 5), u'00045')

    def test_d_preserve_whitespace(self):
        self._test_simple_text_action(u'  78 ', ReformatAction('d'), u'  78 ')
        self._test_simple_text_action(u'  78 ', ReformatAction('d', 3), u'  078 ')

    def test_d_non_number(self):
        with self.assertRaises(SpecifierExpectsNumberException):
            self._test_simple_text_action(u'00abc', ReformatAction('d'), u'should fail')
