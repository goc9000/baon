import antlr3

from genparsers.RulesLexer import RulesLexer
from genparsers.RulesParser import RulesParser

class RuleParser(object):
    '''
    Note: this is currently just a thin wrapper for the ANTLR3-generated class.
    '''

    def __init__(self):
        pass
    
    def parse(self, ruleText):
        chrStream = antlr3.ANTLRStringStream(ruleText)
        lexer = RulesLexer(chrStream)
        tokStream = antlr3.CommonTokenStream(lexer)
        parser = RulesParser(tokStream)
        
        try:
            ruleset = parser.ruleset()
            
            return ruleset
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
