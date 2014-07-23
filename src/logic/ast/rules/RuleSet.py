# logic/ast/rules/RuleSet.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.ASTNode import ASTNode, ast_node_children

from logic.rules.MatchContext import MatchContext
from logic.rules.SemanticCheckScope import SemanticCheckScope


class RuleSet(ASTNode):
    rules = ast_node_children()
    
    def __init__(self):
        ASTNode.__init__(self)
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

    def is_empty(self):
        return len(self.rules) == 0
