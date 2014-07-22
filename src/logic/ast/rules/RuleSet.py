# logic/ast/rules/RuleSet.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.RulesASTNode import RulesASTNode

from logic.rules.MatchContext import MatchContext
from logic.rules.SemanticCheckScope import SemanticCheckScope


class RuleSet(RulesASTNode):
    rules = None
    
    def __init__(self):
        RulesASTNode.__init__(self)
        self.rules = []

    def applyOn(self, text, initial_aliases=None):
        for rule in self.rules:
            context = MatchContext(text, initial_aliases)
            matched = rule.execute(context)
            
            if (matched is not False) and (len(context.forward_aliases) > 0):
                context = MatchContext(text, context.aliases)
                matched = rule.execute(context)
            
            if matched is not False:
                text = matched + context.text[context.position:]
                
            if context.stop:
                break
            
        return text

    def isEmpty(self):
        return len(self.rules) == 0
    
    def semanticCheck(self, scope=None):
        if scope is None:
            scope = SemanticCheckScope
        
        for rule in self.rules:
            rule.semanticCheck(scope)

    def _test_repr_node_name(self):
        return 'RULE_SET'

    def _test_repr_children(self):
        return self.rules
