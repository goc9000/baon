from SemanticCheckScope import SemanticCheckScope

class RuleSet(object):
    rules = None
    
    def __init__(self):
        self.rules = []

    def applyOn(self, text):
        return "<todo>"

    def isEmpty(self):
        return len(self.rules) == 0
    
    def semanticCheck(self, scope=None):
        if scope is None:
            scope = SemanticCheckScope
        
        for rule in self.rules:
            rule.semanticCheck(scope)
