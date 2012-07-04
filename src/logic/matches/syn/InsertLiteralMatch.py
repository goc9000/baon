from InsertionMatch import InsertionMatch

class InsertLiteralMatch(InsertionMatch):
    text = None
    
    def __init__(self, text):
        InsertionMatch.__init__(self)

        self.text = text
    
    def _execute(self, context):
        context.last_match_pos = None
        
        return self.text