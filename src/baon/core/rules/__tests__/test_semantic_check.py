# baon/core/rules/__tests__/test_semantic_check.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.core.ast.rule_check_exceptions import RuleCheckException
from baon.core.rules.RuleSet import RuleSet


class TestSemanticCheck(TestCase):

    def test_check_regex_match(self):
        self.assertEqual(self.check_result(u'/abc/i'),
                         True)
        self.assertEqual(self.check_result(u'/[abc/'),
                         ('ErrorInRegularExpressionException', 1, 1, 1, 6))
        self.assertEqual(self.check_result(u'/abc/QXYZ'),
                         ('InvalidRegexFlagException', {'flag': u'Q'}, 1, 1, 1, 9))

    def test_check_format_match(self):
        self.assertEqual(self.check_result(u'%4d'),
                         True)
        self.assertEqual(self.check_result(u'%bogus'),
                         ('UnrecognizedFormatSpecifierException', {'specifier': u'bogus'}, 1, 1, 1, 6))
        self.assertEqual(self.check_result(u'%0s'),
                         ('WidthMustBeAtLeast1ForSpecifierException', {'specifier': u's'}, 1, 1, 1, 3))
        self.assertEqual(self.check_result(u'%0c'),
                         ('WidthMustBeAtLeast1ForSpecifierException', {'specifier': u'c'}, 1, 1, 1, 3))
        self.assertEqual(self.check_result(u'%0ws'),
                         True)
        self.assertEqual(self.check_result(u'%4path'),
                         ('WidthInapplicableToSpecifierException', {'specifier': u'path'}, 1, 1, 1, 6))
        self.assertEqual(self.check_result(u'%05s'),
                         ("Leading0sInapplicableToSpecifierException", {'specifier': u's'}, 1, 1, 1, 4))

    def test_check_apply_function_action(self):
        self.assertEqual(self.check_result(u'%s->title'),
                         True)
        self.assertEqual(self.check_result(u'%s->tilte'),
                         ('UnsupportedFunctionException', {'function_name': u'tilte'}, 1, 3, 1, 9))

    def test_check_apply_rule_set_action_checks_inside_rule_set(self):
        self.assertEqual(self.check_result(u'%s->(%d)'),
                         True)
        self.assertEqual(self.check_result(u'%s->(%bogus)'),
                         ('UnrecognizedFormatSpecifierException', {'specifier': u'bogus'}, 1, 6, 1, 11))
        self.assertEqual(self.check_result(u'%s->(%d->(..->tilte))'),
                         ('UnsupportedFunctionException', {'function_name': u'tilte'}, 1, 13, 1, 19))

    def test_check_reformat_action(self):
        self.assertEqual(self.check_result(u'%d->%d'),
                         True)
        self.assertEqual(self.check_result(u'%d->%3d'),
                         True)
        self.assertEqual(self.check_result(u'%d->%04d'),
                         True)
        self.assertEqual(self.check_result(u'%d->%s'),
                         ('UnrecognizedFormatSpecifierException', {'specifier': u's'}, 1, 3, 1, 6))
        self.assertEqual(self.check_result(u'%d->%0d'),
                         ('WidthMustBeAtLeast1ForSpecifierException', {'specifier': u'd'}, 1, 3, 1, 7))

    def test_check_match_sequence(self):
        self.assertEqual(self.check_result(u'%d %bogus %s'),
                         ('UnrecognizedFormatSpecifierException', {'specifier': u'bogus'}, 1, 4, 1, 9))
        self.assertEqual(self.check_result(u'%d %first %second %s'),
                         ('UnrecognizedFormatSpecifierException', {'specifier': u'first'}, 1, 4, 1, 9))

    def test_check_repeat_match(self):
        self.assertEqual(self.check_result(u'%d->bogus+'),
                         ('UnsupportedFunctionException', {'function_name': u'bogus'}, 1, 3, 1, 9))

    def test_check_subrule_match_checks_inside_rule(self):
        self.assertEqual(self.check_result(u'%s (%d)'),
                         True)
        self.assertEqual(self.check_result(u'%s (%bogus)'),
                         ('UnrecognizedFormatSpecifierException', {'specifier': u'bogus'}, 1, 5, 1, 10))
        self.assertEqual(self.check_result(u'%s (%d (..->tilte))'),
                         ('UnsupportedFunctionException', {'function_name': u'tilte'}, 1, 11, 1, 17))

    def check_result(self, text_input):
        try:
            RuleSet.from_source(text_input)
        except RuleCheckException as e:
            return e.test_repr()

        return True
