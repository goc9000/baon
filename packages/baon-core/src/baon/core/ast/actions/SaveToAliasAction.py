# baon/core/ast/actions/SaveToAliasAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.actions.Action import Action
from baon.core.ast.ASTNode import ast_node_field


class SaveToAliasAction(Action):
    alias = ast_node_field()
    
    def __init__(self, alias):
        Action.__init__(self)
        
        self.alias = alias
    
    def execute(self, action_context):
        new_aliases = dict(action_context.aliases)
        new_aliases[self.alias] = action_context.text

        return action_context._replace(aliases=new_aliases)
