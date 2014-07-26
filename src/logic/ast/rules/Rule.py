# logic/ast/rules/Rule.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.ASTNode import ASTNode, ast_node_child


class Rule(ASTNode):
    content = ast_node_child()
    
    def __init__(self, content):
        ASTNode.__init__(self)
        self.content = content

    def is_empty(self):
        return self.content.is_empty()

    def execute(self, context):
        return self.content.execute(context)
