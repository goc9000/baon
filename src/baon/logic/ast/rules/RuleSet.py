# baon/logic/ast/rules/RuleSet.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.ASTNode import ASTNode, ast_node_children
from baon.logic.rules.ApplyRuleResult import ApplyRuleResult


class RuleSet(ASTNode):
    rules = ast_node_children()
    
    def __init__(self):
        ASTNode.__init__(self)
        self.rules = []

    def is_empty(self):
        return len(self.rules) == 0

    def add_rule(self, rule):
        self.rules.append(rule)
        return self

    def apply_on(self, text, aliases=None):
        result = ApplyRuleResult(text=text, aliases=aliases if aliases is None else dict())

        for rule in self.rules:
            result = rule.apply_on(result.text, result.aliases)

        return result
