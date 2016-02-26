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
        self._test_simple_text_action('acE oF bAsE', ApplyFunctionAction('title'), 'Ace of Base')
        self._test_simple_text_action('acE oF bAsE', ApplyFunctionAction('upper'), 'ACE OF BASE')
        self._test_simple_text_action('acE oF bAsE', ApplyFunctionAction('toupper'), 'ACE OF BASE')
        self._test_simple_text_action('acE oF bAsE', ApplyFunctionAction('lower'), 'ace of base')
        self._test_simple_text_action('acE oF bAsE', ApplyFunctionAction('tolower'), 'ace of base')

    def test_whitespace_functions(self):
        self._test_simple_text_action('  trim me ', ApplyFunctionAction('trim'), 'trim me')

    def test_unbrace(self):
        self._test_simple_text_action('(abc)', ApplyFunctionAction('unbrace'), 'abc')

    def test_add_brace_functions(self):
        self._test_simple_text_action('abc', ApplyFunctionAction('parens'), '(abc)')
        self._test_simple_text_action('abc', ApplyFunctionAction('braces'), '[abc]')
        self._test_simple_text_action('abc', ApplyFunctionAction('curlies'), '{abc}')

    def test_extract_in_braces_functions(self):
        self._test_simple_text_action('ab(cde)f', ApplyFunctionAction('inparens'), 'cde')
        self._test_simple_text_action('ab[cde]f', ApplyFunctionAction('inbraces'), 'cde')
        self._test_simple_text_action('ab{cde}f', ApplyFunctionAction('incurlies'), 'cde')
