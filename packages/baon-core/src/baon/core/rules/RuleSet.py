# baon/core/rules/RuleSet.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import baon.core.ast.rules.RuleSet

from baon.core.parsing.parse_rules import parse_rules
from baon.core.rules.SemanticCheckScope import SemanticCheckScope


class RuleSet(object):
    _rule_set_node = None

    def __init__(self, rule_set_node=None):
        if rule_set_node is None:
            rule_set_node = baon.core.ast.rules.RuleSet.RuleSet()

        self._rule_set_node = rule_set_node
        self._rule_set_node.semantic_check(SemanticCheckScope())

    def apply_on(self, text, aliases=None):
        return self._rule_set_node.apply_on(text, aliases)

    @staticmethod
    def from_source(rules_text):
        return RuleSet(parse_rules(rules_text))
