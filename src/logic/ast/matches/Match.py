# logic/ast/matches/Match.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.ASTNode import ASTNode, ast_node_children


class Match(ASTNode):
    actions = ast_node_children()

    def __init__(self):
        ASTNode.__init__(self)
        self.actions = []

    def execute(self, context):
        savept = context.save()
            
        text = self._execute(context)

        if text is not False:
            for action in self.actions:
                text = action.execute(text, context)
                if text is False:
                    break
        
        if text is False:
            context.restore(savept)
            context.last_match_pos = None
        
        return text

    def _execute(self, context):
        raise RuntimeError("_test_repr_impl() not implemented in subclass")
