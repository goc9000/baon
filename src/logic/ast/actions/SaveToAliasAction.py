# logic/ast/actions/SaveToAliasAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.actions.Action import Action
from logic.ast.ASTNode import ast_node_field


class SaveToAliasAction(Action):
    alias = ast_node_field()
    
    def __init__(self, alias):
        Action.__init__(self)
        
        self.alias = alias
    
    def execute(self, context):
        new_aliases = dict(context.aliases)
        new_aliases[self.alias] = context.matched_text

        return context._replace(aliases=new_aliases)
