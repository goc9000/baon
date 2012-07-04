from Action import Action
from logic.RuleCheckException import RuleCheckException

def is_particle(word):
    return word in ['a','an','of','with','for','in','on']

def to_title_case(s):
    words = s.split(' ')
    first = True

    for i in xrange(len(words)):
        word = words[i]
        if word == '':
            continue

        if first or not is_particle(word.lower()):
            words[i] = word.capitalize()
        else:
            words[i] = word.lower()

        first = False
    
    return ' '.join(words)

class ApplyFunctionAction(Action):
    fn = None
    error = None
    
    def __init__(self, fn_name):
        Action.__init__(self)
        
        if fn_name=="title":
            self.fn = lambda s,c: to_title_case(s)
        elif fn_name=="trim":
            self.fn = lambda s,c: s.strip()
        elif fn_name=="upper" or fn_name=="toupper":
            self.fn = lambda s,c: s.upper()
        elif fn_name=="lower" or fn_name=="tolower":
            self.fn = lambda s,c: s.lower()
        else:
            self.error = "Unsupported function '{0}'".format(fn_name)
    
    def semanticCheck(self, scope):
        Action.semanticCheck(self, scope)
        
        if not self.error is None:
            raise RuleCheckException(self.error, scope)

    def execute(self, text, context):
        return self.fn(text, context)
