# logic/parsing/RulesParser.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from ply import yacc
from ply.yacc import NullLogger

from logic.rules.RuleSet import RuleSet
from logic.rules.Rule import Rule
from logic.matches.special.MatchSequence import MatchSequence
from logic.matches.StartAnchorMatch import StartAnchorMatch
from logic.matches.EndAnchorMatch import EndAnchorMatch
from logic.matches.LiteralMatch import LiteralMatch
from logic.matches.RegexMatch import RegexMatch
from logic.matches.FormatMatch import FormatMatch

from logic.errors.RuleParseException import RuleParseException

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


def p_match_literal(p):
    """match : STRING_LITERAL"""
    literal_info = p[1].extras
    if 'unterminated' in literal_info and literal_info['unterminated']:
        raise RuleParseException.from_token(p[1], "Unterminated string")
    if 'error' in literal_info:
        raise RuleParseException.from_token(p[1], literal_info['error'])

    p[0] = LiteralMatch(p[1].extras['value'])


def p_match_regex(p):
    """match : REGEX"""
    regex_info = p[1].extras
    if 'unterminated' in regex_info and regex_info['unterminated']:
        raise RuleParseException.from_token(p[1], "Unterminated regex")

    flags = regex_info['flags'] if 'flags' in regex_info else set()
    p[0] = RegexMatch(regex_info['pattern'], flags)


def p_match_format(p):
    """match : FORMAT_SPEC"""
    spec_info = p[1].extras
    specifier = spec_info['specifier'] if 'specifier' in spec_info else None
    width = spec_info['width'] if 'width' in spec_info else None
    leading_zeros = spec_info['leading_zeros'] if 'leading_zeros' in spec_info else None

    if specifier is None:
        raise RuleParseException.from_token(p[1], "Missing format specifier")

    p[0] = FormatMatch(specifier, width, leading_zeros)


start = 'rule_set'

parser_template = yacc.yacc()


class RulesParser(object):
    @staticmethod
    def parse(rules_text):
        return parser_template.parse(rules_text, RulesLexerForYACC())

    @staticmethod
    def debug_parse(rules_text, start_rule):
        parser = yacc.yacc(start=start_rule, debug=0, errorlog=NullLogger())
        return parser.parse(rules_text, RulesLexerForYACC())


class RulesLexerForYACC(object):
    _token_stream = None

    def __init__(self):
        pass

    def input(self, rules_text):
        self._token_stream = RulesLexer.tokenize(rules_text)

    def token(self):
        return next(self._token_stream, None)
