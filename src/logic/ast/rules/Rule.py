# logic/ast/rules/Rule.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.ASTNode import ASTNode, ast_node_children


class Rule(ASTNode):
    alternatives = ast_node_children()
    
    def __init__(self):
        ASTNode.__init__(self)
        self.alternatives = []

    def is_empty(self):
        return (len(self.alternatives) == 0) or all(alt.is_empty() for alt in self.alternatives)

    def semanticCheck(self, scope):
        for alt in self.alternatives:
            alt.semanticCheck(scope)

    def execute(self, context):
        for alt in self.alternatives:
            matched = alt.execute(context)

            if matched is not False:
                return matched
        
        return False
