import antlr3

from genparser.RulesLexer import RulesLexer
from genparser.RulesParser import RulesParser

class RuleParser(object):
    '''
    Note: this is currently a wrapper for the ANTLR3-generated class. It was
    made like this to enable changing the backend if needed
    '''

    def __init__(self):
        pass
    
    def parse(self, ruleText):
        chrStream = antlr3.ANTLRStringStream(ruleText)
        lexer = RulesLexer(chrStream)
        tokStream = antlr3.CommonTokenStream(lexer)
        parser = RulesParser(tokStream)
        
        try:
            parser.xruleset()
        except antlr3.RecognitionException as e:
            raise RuleParseException("Syntax error", e.line-1, e.charPositionInLine)
        
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
