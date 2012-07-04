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
