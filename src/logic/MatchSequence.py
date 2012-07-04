class MatchSequence(object):
    terms = None

    def __init__(self):
        self.terms = []

    def semanticCheck(self, scope):
        #todo: check for consecutive '..' s etc.
        
        for term in self.terms:
            term.semanticCheck(scope)

    def execute(self, context):
        savept = context.save()
        committed = []

        for term in self.terms:
            matched = term.execute(context)

            if matched is False:
                context.restore(savept)
                return False

            committed.append(matched)

        return ''.join(committed)
