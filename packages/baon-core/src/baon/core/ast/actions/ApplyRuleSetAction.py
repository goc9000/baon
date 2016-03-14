# baon/core/ast/actions/ApplyRuleSetAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.actions.Action import Action
from baon.core.ast.ASTNode import ast_node_child


class ApplyRuleSetAction(Action):
    ruleset = ast_node_child()
    
    def __init__(self, ruleset):
        Action.__init__(self)
        
        self.ruleset = ruleset

    def execute(self, action_context):
        new_text, new_aliases = self.ruleset.apply_on(action_context.text, action_context.aliases)

        return action_context._replace(text=new_text, aliases=new_aliases)
