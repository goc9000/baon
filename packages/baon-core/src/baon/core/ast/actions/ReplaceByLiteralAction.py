# baon/core/ast/actions/ReplaceByLiteralAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.actions.Action import Action
from baon.core.ast.ASTNode import ast_node_field


class ReplaceByLiteralAction(Action):
    text = ast_node_field()
    
    def __init__(self, text):
        Action.__init__(self)

        self.text = text

    def execute(self, context):
        return context._replace(matched_text=self.text)
