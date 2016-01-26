# baon/core/rules/__tests__/test_semantic_check.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.core.ast.__errors__.rule_check_errors import RuleCheckError
from baon.core.rules.RuleSet import RuleSet


class TestSemanticCheck(TestCase):

    def test_check_regex_match(self):
        self.assertEqual(self.check_result('/abc/i'),
                         True)
        self.assertEqual(self.check_result('/[abc/'),
                         ('ErrorInRegularExpressionError', 1, 1, 1, 6))
        self.assertEqual(self.check_result('/abc/Qi'),
                         ('InvalidRegexFlagError', {'flag': 'Q'}, 1, 1, 1, 7))

    def test_check_format_match(self):
        self.assertEqual(self.check_result('%4d'),
                         True)
        self.assertEqual(self.check_result('%bogus'),
                         ('UnrecognizedFormatSpecifierError', {'specifier': 'bogus'}, 1, 1, 1, 6))
        self.assertEqual(self.check_result('%0s'),
                         ('WidthMustBeAtLeast1ForSpecifierError', {'specifier': 's'}, 1, 1, 1, 3))
        self.assertEqual(self.check_result('%0c'),
                         ('WidthMustBeAtLeast1ForSpecifierError', {'specifier': 'c'}, 1, 1, 1, 3))
        self.assertEqual(self.check_result('%0ws'),
                         True)
        self.assertEqual(self.check_result('%4path'),
                         ('WidthInapplicableToSpecifierError', {'specifier': 'path'}, 1, 1, 1, 6))
        self.assertEqual(self.check_result('%05s'),
                         ('Leading0sInapplicableToSpecifierError', {'specifier': 's'}, 1, 1, 1, 4))

    def test_check_apply_function_action(self):
        self.assertEqual(self.check_result('%s->title'),
                         True)
        self.assertEqual(self.check_result('%s->tilte'),
                         ('UnsupportedFunctionError', {'function_name': 'tilte'}, 1, 3, 1, 9))

    def test_check_apply_rule_set_action_checks_inside_rule_set(self):
        self.assertEqual(self.check_result('%s->(%d)'),
                         True)
        self.assertEqual(self.check_result('%s->(%bogus)'),
                         ('UnrecognizedFormatSpecifierError', {'specifier': 'bogus'}, 1, 6, 1, 11))
        self.assertEqual(self.check_result('%s->(%d->(..->tilte))'),
                         ('UnsupportedFunctionError', {'function_name': 'tilte'}, 1, 13, 1, 19))

    def test_check_reformat_action(self):
        self.assertEqual(self.check_result('%d->%d'),
                         True)
        self.assertEqual(self.check_result('%d->%3d'),
                         True)
        self.assertEqual(self.check_result('%d->%04d'),
                         True)
        self.assertEqual(self.check_result('%d->%s'),
                         ('UnrecognizedFormatSpecifierError', {'specifier': 's'}, 1, 3, 1, 6))
        self.assertEqual(self.check_result('%d->%0d'),
                         ('WidthMustBeAtLeast1ForSpecifierError', {'specifier': 'd'}, 1, 3, 1, 7))

    def test_check_match_sequence(self):
        self.assertEqual(self.check_result('%d %bogus %s'),
                         ('UnrecognizedFormatSpecifierError', {'specifier': 'bogus'}, 1, 4, 1, 9))
        self.assertEqual(self.check_result('%d %first %second %s'),
                         ('UnrecognizedFormatSpecifierError', {'specifier': 'first'}, 1, 4, 1, 9))

    def test_check_repeat_match(self):
        self.assertEqual(self.check_result('%d->bogus+'),
                         ('UnsupportedFunctionError', {'function_name': 'bogus'}, 1, 3, 1, 9))

    def test_check_subrule_match_checks_inside_rule(self):
        self.assertEqual(self.check_result('%s (%d)'),
                         True)
        self.assertEqual(self.check_result('%s (%bogus)'),
                         ('UnrecognizedFormatSpecifierError', {'specifier': 'bogus'}, 1, 5, 1, 10))
        self.assertEqual(self.check_result('%s (%d (..->tilte))'),
                         ('UnsupportedFunctionError', {'function_name': 'tilte'}, 1, 11, 1, 17))

    def check_result(self, text_input):
        try:
            RuleSet.from_source(text_input)
        except RuleCheckError as e:
            return e.test_repr()

        return True
