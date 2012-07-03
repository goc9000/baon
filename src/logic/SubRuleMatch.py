from Match import Match

class SubRuleMatch(Match):
    rule = None
    
    def __init__(self, rule):
        Match.__init__(self)
        
        self.rule = rule

    def semanticCheck(self, scope):
        self.rule.semanticCheck(scope)
        
        Match.semanticCheck(self, scope)