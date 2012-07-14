# logic/actions/ApplyRuleSetAction.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from Action import Action

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
