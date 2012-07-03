from Action import Action
from RuleCheckException import RuleCheckException

class ReformatAction(Action):
    error = None
    fn = None
    
    def __init__(self, fmt_spec):
        Action.__init__(self)
        
        self.error="Unrecognized format specifier '{0}'".format(fmt_spec)
    
    def semanticCheck(self, scope):
        Action.semanticCheck(self, scope)
        
        if not self.error is None:
            raise RuleCheckException(self.error, scope)
