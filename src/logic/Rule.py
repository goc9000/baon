class Rule(object):
    alternatives = None
    
    def __init__(self):
        self.alternatives = []

    def semanticCheck(self, scope):
        for alt in self.alternatives:
            alt.semanticCheck(scope)

    def execute(self, context):
        for alt in self.alternatives:
            matched = alt.execute(context)

            if matched is not False:
                return matched
        
        return False
