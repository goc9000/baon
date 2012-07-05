class RuleCheckException(Exception):
    message = None
    scope = None
    
    def __init__(self, message, scope):
        self.message = message
        self.scope = scope
    
    def __str__(self):
        return self.message
