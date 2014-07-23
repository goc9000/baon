# logic/rules/__tests__/test_semantic_check.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from logic.errors.RuleCheckException import RuleCheckException

from logic.rules.RulesCompiler import RulesCompiler


class TestSemanticCheck(TestCase):

    def test_check_regex_match(self):
        self.assertEqual(self.check_result(u'/abc/i'),
                         True)
        self.assertEqual(self.check_result(u'/[abc/'),
                         ('RuleCheckException', 'Error in regular expression', 1, 1, 1, 6))
        self.assertEqual(self.check_result(u'/abc/QXYZ'),
                         ('RuleCheckException', "Invalid regex flag 'Q'", 1, 1, 1, 9))

    def test_check_format_match(self):
        self.assertEqual(self.check_result(u'%4d'),
                         True)
        self.assertEqual(self.check_result(u'%bogus'),
                         ('RuleCheckException', "Unrecognized format specifier 'bogus'", 1, 1, 1, 6))
        self.assertEqual(self.check_result(u'%0s'),
                         ('RuleCheckException', "Width must be at least 1 for specifier 's'", 1, 1, 1, 3))
        self.assertEqual(self.check_result(u'%0c'),
                         ('RuleCheckException', "Width must be at least 1 for specifier 'c'", 1, 1, 1, 3))
        self.assertEqual(self.check_result(u'%0ws'),
                         True)
        self.assertEqual(self.check_result(u'%4path'),
                         ('RuleCheckException', "Width inapplicable to specifier 'path'", 1, 1, 1, 6))
        self.assertEqual(self.check_result(u'%05s'),
                         ('RuleCheckException', "Leading 0s inapplicable to specifier 's'", 1, 1, 1, 4))

    def check_result(self, text_input):
        try:
            RulesCompiler.check_rules(text_input)
        except RuleCheckException as e:
            return e.test_repr()

        return True
