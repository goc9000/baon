# baon/logic/ast/actions/ApplyRuleSetAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.actions.Action import Action
from baon.logic.ast.ASTNode import ast_node_child


class ApplyRuleSetAction(Action):
    ruleset = ast_node_child()
    
    def __init__(self, ruleset):
        Action.__init__(self)
        
        self.ruleset = ruleset

    def execute(self, context):
        new_text, new_aliases = self.ruleset.apply_on(context.matched_text, context.aliases)

        return context._replace(
            matched_text=new_text,
            aliases=new_aliases,
        )
