class MatchSequence(object):
    terms = None

    def __init__(self):
        self.terms = []

    def semanticCheck(self, scope):
        #todo: check for consecutive '..' s etc.
        
        for term in self.terms:
            term.semanticCheck(scope)
