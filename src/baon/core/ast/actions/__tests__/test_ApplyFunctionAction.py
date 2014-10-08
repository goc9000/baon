# baon/core/ast/actions/__tests__/test_ApplyFunctionAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.actions.__tests__.ActionTestCase import ActionTestCase
from baon.core.ast.actions.ApplyFunctionAction import ApplyFunctionAction


class TestApplyFunctionAction(ActionTestCase):

    def test_case_functions(self):
        # Note: these are only superficial tests of each function, mainly to verify that each is supported.
        # Complex functions and their special cases are tested in their dedicated unittests.
        self._test_simple_text_action(u'acE oF bAsE', ApplyFunctionAction('title'), u'Ace of Base')
        self._test_simple_text_action(u'acE oF bAsE', ApplyFunctionAction('upper'), u'ACE OF BASE')
        self._test_simple_text_action(u'acE oF bAsE', ApplyFunctionAction('toupper'), u'ACE OF BASE')
        self._test_simple_text_action(u'acE oF bAsE', ApplyFunctionAction('lower'), u'ace of base')
        self._test_simple_text_action(u'acE oF bAsE', ApplyFunctionAction('tolower'), u'ace of base')

    def test_whitespace_functions(self):
        self._test_simple_text_action(u'  trim me ', ApplyFunctionAction('trim'), u'trim me')

    def test_unbrace(self):
        self._test_simple_text_action(u'(abc)', ApplyFunctionAction('unbrace'), u'abc')

    def test_add_brace_functions(self):
        self._test_simple_text_action(u'abc', ApplyFunctionAction('paras'), u'(abc)')
        self._test_simple_text_action(u'abc', ApplyFunctionAction('braces'), u'[abc]')
        self._test_simple_text_action(u'abc', ApplyFunctionAction('curlies'), u'{abc}')

    def test_extract_in_braces_functions(self):
        self._test_simple_text_action(u'ab(cde)f', ApplyFunctionAction('inparas'), u'cde')
        self._test_simple_text_action(u'ab[cde]f', ApplyFunctionAction('inbraces'), u'cde')
        self._test_simple_text_action(u'ab{cde}f', ApplyFunctionAction('incurlies'), u'cde')
