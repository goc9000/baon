from InsertionMatch import InsertionMatch

class InsertLiteralMatch(InsertionMatch):
    text = None
    
    def __init__(self, text):
        InsertionMatch.__init__(self)

        self.text = text
    
    def execute(self, context):
        return self.text