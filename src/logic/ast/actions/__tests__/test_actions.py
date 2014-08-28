# logic/ast/actions/__tests__/test_actions.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from logic.rules.MatchContext import MatchContext

from logic.ast.actions.ApplyFunctionAction import ApplyFunctionAction
from logic.ast.actions.DeleteAction import DeleteAction
from logic.ast.actions.ReformatAction import ReformatAction
from logic.ast.actions.ReplaceByLiteralAction import ReplaceByLiteralAction
from logic.ast.actions.SaveToAliasAction import SaveToAliasAction

from logic.errors.RuleApplicationException import RuleApplicationException


class TestActions(TestCase):

    def test_apply_function_action(self):
        # TODO: Add dedicated unit tests for every function in separate unit

        # Note: these are only superficial tests of each function, mainly to verify that each is supported.
        # Complex functions and their special cases are tested in their dedicated unittests.
        self._test_simple_text_action(u'acE oF bAsE', ApplyFunctionAction('title'), u'Ace of Base')
        self._test_simple_text_action(u'acE oF bAsE', ApplyFunctionAction('upper'), u'ACE OF BASE')
        self._test_simple_text_action(u'acE oF bAsE', ApplyFunctionAction('toupper'), u'ACE OF BASE')
        self._test_simple_text_action(u'acE oF bAsE', ApplyFunctionAction('lower'), u'ace of base')
        self._test_simple_text_action(u'acE oF bAsE', ApplyFunctionAction('tolower'), u'ace of base')
        self._test_simple_text_action(u'  trim me ', ApplyFunctionAction('trim'), u'trim me')
        self._test_simple_text_action(u'(abc)', ApplyFunctionAction('unbrace'), u'abc')
        self._test_simple_text_action(u'abc', ApplyFunctionAction('paras'), u'(abc)')
        self._test_simple_text_action(u'abc', ApplyFunctionAction('braces'), u'[abc]')
        self._test_simple_text_action(u'abc', ApplyFunctionAction('curlies'), u'{abc}')
        self._test_simple_text_action(u'ab(cde)f', ApplyFunctionAction('inparas'), u'cde')
        self._test_simple_text_action(u'ab[cde]f', ApplyFunctionAction('inbraces'), u'cde')
        self._test_simple_text_action(u'ab{cde}f', ApplyFunctionAction('incurlies'), u'cde')

    # TODO: Add test_apply_rule_set_action (when RuleSet support is solid)

    def test_delete_action(self):
        self._test_simple_text_action(u'Some text', DeleteAction(), u'')
        self._test_simple_text_action(u'', DeleteAction(), u'')

    def test_reformat_action(self):
        self._test_simple_text_action(u'123', ReformatAction('d'), u'123')
        self._test_simple_text_action(u'0045', ReformatAction('d'), u'45')
        self._test_simple_text_action(u'  78 ', ReformatAction('d'), u'  78 ')

        self._test_simple_text_action(u'1234', ReformatAction('d', 3), u'1234')
        self._test_simple_text_action(u'0045', ReformatAction('d', 3), u'045')
        self._test_simple_text_action(u'  78 ', ReformatAction('d', 3), u'  078 ')

        with self.assertRaisesRegexp(RuleApplicationException, 'non-number'):
            self._test_simple_text_action(u'00abc', ReformatAction('d'), u'should fail')

    def test_replace_by_literal_action(self):
        self._test_simple_text_action(u'Some text', ReplaceByLiteralAction(u'Other text'), u'Other text')
        self._test_simple_text_action(u'', ReplaceByLiteralAction(u'Some text'), u'Some text')
        self._test_simple_text_action(u'', ReplaceByLiteralAction(u''), u'')

    def test_save_to_alias_action(self):
        self._test_aliases_action(
            dict(),
            SaveToAliasAction(u'alias'),
            {u'alias': u'Matched text'}
        )
        self._test_aliases_action(
            {u'alias': u'Previous text'},
            SaveToAliasAction(u'alias'),
            {u'alias': u'Matched text'}
        )
        self._test_aliases_action(
            {u'alias': u'Previous text'},
            SaveToAliasAction(u'new_alias'),
            {u'alias': u'Previous text', u'new_alias': u'Matched text'}
        )

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

    def _test_aliases_action(self, aliases, action, expected_aliases):
        test_context = MatchContext(
            text=u'ignored',
            position=0,
            aliases=aliases,
            matched_text=u'Matched text',
        )

        result_context = action.execute(test_context)

        self.assertEquals(
            result_context,
            test_context._replace(aliases=expected_aliases)
        )
