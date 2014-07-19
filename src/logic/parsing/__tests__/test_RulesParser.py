# logic/parsing/__tests__/test_RulesParser.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from logic.parsing.RulesParser import RulesParser


class TestRulesLexer(TestCase):

    def test_parse_empty(self):
        self.assertEqual(self.parse_result(u''),
                         ('RULE_SET', ()))
        self.assertEqual(self.parse_result(u';'),
                         ('RULE_SET', ()))
        self.assertEqual(self.parse_result(u'\n'),
                         ('RULE_SET', ()))
        self.assertEqual(self.parse_result(u'  ;  \n ;;\n  \n\n'),
                         ('RULE_SET', ()))

    def parse_result(self, rules_text):
        return RulesParser.parse(rules_text).test_repr()
