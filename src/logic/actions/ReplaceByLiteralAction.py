from Action import Action

class ReplaceByLiteralAction(Action):
    text = None
    
    def __init__(self, text):
        Action.__init__(self)

        self.text = text

    def execute(self, text, context):
        return self.text
