class Match(object):
    actions = None

    def __init__(self):
        self.actions = []

    def semanticCheck(self, scope):
        # This just checks the actions
        for action in self.actions:
            action.semanticCheck(scope)

    def runActions(self, text, scope):
        savept = scope.save()

        for action in self.actions:
            text = action.execute(text, scope)
            if text == False:
                scope.restore(savept)
                return False

        return text
