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

    def test_check_apply_function_action(self):
        self.assertEqual(self.check_result(u'%s->title'),
                         True)
        self.assertEqual(self.check_result(u'%s->tilte'),
                         ('RuleCheckException', "Unsupported function 'tilte'", 1, 3, 1, 9))

    def test_check_apply_rule_set_action_checks_inside_rule_set(self):
        self.assertEqual(self.check_result(u'%s->(%d)'),
                         True)
        self.assertEqual(self.check_result(u'%s->(%bogus)'),
                         ('RuleCheckException', "Unrecognized format specifier 'bogus'", 1, 6, 1, 11))
        self.assertEqual(self.check_result(u'%s->(%d->(..->tilte))'),
                         ('RuleCheckException', "Unsupported function 'tilte'", 1, 13, 1, 19))

    def test_check_reformat_action(self):
        self.assertEqual(self.check_result(u'%d->%d'),
                         True)
        self.assertEqual(self.check_result(u'%d->%3d'),
                         True)
        self.assertEqual(self.check_result(u'%d->%04d'),
                         True)
        self.assertEqual(self.check_result(u'%d->%s'),
                         ('RuleCheckException', "Unrecognized format specifier 's'", 1, 3, 1, 6))
        self.assertEqual(self.check_result(u'%d->%0d'),
                         ('RuleCheckException', "Width must be at least 1 for specifier 'd'", 1, 3, 1, 7))

    def test_check_match_sequence(self):
        self.assertEqual(self.check_result(u'%d %bogus %s'),
                         ('RuleCheckException', "Unrecognized format specifier 'bogus'", 1, 4, 1, 9))
        self.assertEqual(self.check_result(u'%d %first %second %s'),
                         ('RuleCheckException', "Unrecognized format specifier 'first'", 1, 4, 1, 9))

    def test_check_repeat_match(self):
        self.assertEqual(self.check_result(u'%d->bogus+'),
                         ('RuleCheckException', "Unsupported function 'bogus'", 1, 3, 1, 9))

    def test_check_subrule_match_checks_inside_rule(self):
        self.assertEqual(self.check_result(u'%s (%d)'),
                         True)
        self.assertEqual(self.check_result(u'%s (%bogus)'),
                         ('RuleCheckException', "Unrecognized format specifier 'bogus'", 1, 5, 1, 10))
        self.assertEqual(self.check_result(u'%s (%d (..->tilte))'),
                         ('RuleCheckException', "Unsupported function 'tilte'", 1, 11, 1, 17))

    def check_result(self, text_input):
        try:
            RulesCompiler.check_rules(text_input)
        except RuleCheckException as e:
            return e.test_repr()

        return True
