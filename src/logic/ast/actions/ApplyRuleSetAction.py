# logic/ast/actions/ApplyRuleSetAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.actions.Action import Action


class ApplyRuleSetAction(Action):
    ruleset = None
    
    def __init__(self, ruleset):
        Action.__init__(self)
        
        self.ruleset = ruleset
    
    def semanticCheck(self, scope):
        Action.semanticCheck(self, scope)
        
        self.ruleset.semanticCheck(scope)

    def execute(self, text, context):
        return self.ruleset.applyOn(text, context.aliases)

    def _test_repr_children(self):
        return self.ruleset,
