class Match(object):
    actions = None

    def __init__(self):
        self.actions = []

    def semanticCheck(self, scope):
        # This just checks the actions
        for action in self.actions:
            action.semanticCheck(scope)
