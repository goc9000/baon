import antlr3

from logic.errors.RuleParseException import RuleParseException
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
            ruleset = parser.main()
            
            return ruleset
        except antlr3.RecognitionException as e:
            raise RuleParseException("Syntax error", e.line-1, e.charPositionInLine)
