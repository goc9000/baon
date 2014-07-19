# logic/parsing/RulesParser.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from ply import yacc

from logic.rules.RuleSet import RuleSet
from logic.rules.Rule import Rule
from logic.matches.special.MatchSequence import MatchSequence
from logic.matches.StartAnchorMatch import StartAnchorMatch
from logic.matches.EndAnchorMatch import EndAnchorMatch

from logic.parsing.RulesLexer import RulesLexer, tokens


def p_rule_set_add_rule(p):
    """rule_set : rule_set RULE_SEP rule"""
    p[0] = p[1]
    if not p[3].isEmpty():
        p[0].rules.append(p[3])


def p_rule_set_base(p):
    """rule_set : rule"""
    p[0] = RuleSet()

    if not p[1].isEmpty():
        p[0].rules.append(p[1])


def p_rule_add_sequence_match(p):
    """rule : rule OP_OR sequence_match"""
    p[0] = p[1]
    p[0].alternatives.append(p[3])


def p_rule_base(p):
    """rule : sequence_match"""
    p[0] = Rule()
    p[0].alternatives.append(p[1])


def p_sequence_match_add_match(p):
    """sequence_match : sequence_match match"""
    p[0] = p[1]
    p[0].terms.append(p[2])


def p_sequence_match_empty(p):
    """sequence_match : """
    p[0] = MatchSequence()


def p_match_anchor_start(p):
    """match : ANCHOR_START"""
    p[0] = StartAnchorMatch()


def p_match_anchor_end(p):
    """match : ANCHOR_END"""
    p[0] = EndAnchorMatch()


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
