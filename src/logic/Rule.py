class Rule(object):
    alternatives = None
    
    def __init__(self):
        self.alternatives = []

    def semanticCheck(self, scope):
        for alt in self.alternatives:
            alt.semanticCheck(scope)
