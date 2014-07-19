# logic/parsing/RulesParser.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from ply import yacc

from logic.rules.RuleSet import RuleSet

from logic.parsing.RulesLexer import RulesLexer, tokens


def p_rule_set_add_rule(p):
    """rule_set : rule_set RULE_SEP rule"""
    p[0] = p[1]
    if p[2] is not None:
        p[0].rules.append(p[2])


def p_rule_set_base(p):
    """rule_set : rule"""
    p[0] = RuleSet()

    if p[1] is not None:
        p[0].rules.append(p[1])


def p_rule_empty(p):
    """rule : """
    pass


start = 'rule_set'

parser_template = yacc.yacc()


class RulesParser(object):
    @staticmethod
    def parse(rules_text):
        return parser_template.parse(rules_text, RulesLexerForYACC())


class RulesLexerForYACC(object):
    _token_stream = None

    def __init__(self):
        pass

    def input(self, rules_text):
        self._token_stream = RulesLexer.tokenize(rules_text)

    def token(self):
        return next(self._token_stream, None)
