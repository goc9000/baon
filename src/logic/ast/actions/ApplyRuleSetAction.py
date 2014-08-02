# logic/ast/actions/ApplyRuleSetAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.actions.Action import Action
from logic.ast.ASTNode import ast_node_child


class ApplyRuleSetAction(Action):
    ruleset = ast_node_child()
    
    def __init__(self, ruleset):
        Action.__init__(self)
        
        self.ruleset = ruleset

    def execute(self, text, context):
        text, new_aliases = self.ruleset.apply_on(text, context.aliases)
        context.aliases.update(new_aliases)
        return text
