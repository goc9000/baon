# logic/rules/RulesCompiler.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.parsing.RulesParser import RulesParser
from logic.rules.SemanticCheckScope import SemanticCheckScope


class RulesCompiler(object):
    @staticmethod
    def check_rules(rules_text):
        ast = RulesParser.parse(rules_text)
        ast.semantic_check(SemanticCheckScope())
