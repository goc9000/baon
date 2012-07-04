class SearchReplaceMatch(object):
    term = None
    
    def __init__(self, term):
        self.term = term
    
    def semanticCheck(self, scope):
        self.term.semanticCheck(scope)
