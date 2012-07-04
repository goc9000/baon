from SemanticCheckScope import SemanticCheckScope
from MatchContext import MatchContext

class RuleSet(object):
    rules = None
    
    def __init__(self):
        self.rules = []

    def applyOn(self, text, initial_aliases = None):
        for rule in self.rules:
            context = MatchContext(text, initial_aliases)
            matched = rule.execute(context)
            
            if (matched is not False) and (len(context.forward_aliases) > 0):
                context = MatchContext(text, context.aliases)
                matched = rule.execute(context)
            
            if matched is not False:
                text = matched + context.text[context.position:]
                
            if context.stop:
                break
            
        return text

    def isEmpty(self):
        return len(self.rules) == 0
    
    def semanticCheck(self, scope=None):
        if scope is None:
            scope = SemanticCheckScope
        
        for rule in self.rules:
            rule.semanticCheck(scope)
