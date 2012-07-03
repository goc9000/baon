class RuleParseException(Exception):
    line = None
    column = None
    message = None
    
    def __init__(self, message, line, col):
        self.message = message
        self.line = line
        self.column = col
        
    def __str__(self):
        return self.message
