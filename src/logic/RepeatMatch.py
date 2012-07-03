from Match import Match

class RepeatMatch(Match):
    match = None
    
    def __init__(self, match):
        Match.__init__(self)
        
        self.match = match

    def semanticCheck(self, scope):
        self.match.semanticCheck(scope)
        
        Match.semanticCheck(self, scope)