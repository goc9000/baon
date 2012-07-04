from Action import Action

class DeleteAction(Action):
    def __init__(self):
        Action.__init__(self)

    def execute(self, text, context):
        return ''
