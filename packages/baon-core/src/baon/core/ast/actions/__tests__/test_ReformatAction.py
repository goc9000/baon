# baon/core/ast/actions/__tests__/test_ReformatAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.__errors__.rule_application_errors import SpecifierExpectsNumberError

from baon.core.ast.actions.__tests__.ActionTestCase import ActionTestCase
from baon.core.ast.actions.ReformatAction import ReformatAction


class TestReformatAction(ActionTestCase):

    def test_d_basic(self):
        self._test_simple_text_action('123', ReformatAction('d'), '123')
        self._test_simple_text_action('0045', ReformatAction('d'), '45')

    def test_d_shorter_length(self):
        self._test_simple_text_action('1234', ReformatAction('d', 3), '1234')
        self._test_simple_text_action('0045', ReformatAction('d', 3), '045')

    def test_d_longer_length(self):
        self._test_simple_text_action('1234', ReformatAction('d', 5), '01234')
        self._test_simple_text_action('0045', ReformatAction('d', 5), '00045')

    def test_d_preserve_whitespace(self):
        self._test_simple_text_action('  78 ', ReformatAction('d'), '  78 ')
        self._test_simple_text_action('  78 ', ReformatAction('d', 3), '  078 ')

    def test_d_non_number(self):
        with self.assertRaises(SpecifierExpectsNumberError):
            self._test_simple_text_action('00abc', ReformatAction('d'), 'should fail')
