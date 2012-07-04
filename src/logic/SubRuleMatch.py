from Match import Match

class SubRuleMatch(Match):
    rule = None
    
    def __init__(self, rule):
        Match.__init__(self)
        
        self.rule = rule

    def _semanticCheck(self, scope):
        self.rule.semanticCheck(scope)

    def _execute(self, context):
        return self.rule.execute(context)
