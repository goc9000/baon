# logic/ast/rules/RuleSet.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.ASTNode import ASTNode, ast_node_children
from logic.rules.ApplyRuleResult import ApplyRuleResult


class RuleSet(ASTNode):
    rules = ast_node_children()
    
    def __init__(self):
        ASTNode.__init__(self)
        self.rules = []

    def apply_on(self, text, aliases=None):
        result = ApplyRuleResult(text=text, aliases=aliases if aliases is None else dict())

        for rule in self.rules:
            result = rule.apply_on(result.text, result.aliases)

        return result

    def is_empty(self):
        return len(self.rules) == 0
