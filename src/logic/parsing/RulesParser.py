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
from logic.matches.special.RepeatMatch import RepeatMatch

from logic.matches.StartAnchorMatch import StartAnchorMatch
from logic.matches.EndAnchorMatch import EndAnchorMatch
from logic.matches.special.BetweenMatch import BetweenMatch

from logic.matches.pattern.LiteralMatch import LiteralMatch
from logic.matches.pattern.RegexMatch import RegexMatch
from logic.matches.pattern.FormatMatch import FormatMatch

from logic.matches.syn.InsertLiteralMatch import InsertLiteralMatch
from logic.matches.syn.InsertAliasMatch import InsertAliasMatch

from logic.actions.DeleteAction import DeleteAction
from logic.actions.SaveToAliasAction import SaveToAliasAction
from logic.actions.ReplaceByLiteralAction import ReplaceByLiteralAction
from logic.actions.ApplyFunctionAction import ApplyFunctionAction
from logic.actions.ReformatAction import ReformatAction

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


def p_match_add_actions(p):
    """match : match action"""
    p[0] = p[1]
    p[0].actions.append(p[2])


def p_match_add_repeat(p):
    """match : match OP_REPEAT"""
    p[0] = RepeatMatch(p[1], p[2].extras['min'], p[2].extras['max'])


def p_match_anchor_start(p):
    """match : ANCHOR_START"""
    p[0] = StartAnchorMatch()


def p_match_anchor_end(p):
    """match : ANCHOR_END"""
    p[0] = EndAnchorMatch()


def p_match_between(p):
    """match : BETWEEN"""
    p[0] = BetweenMatch()


def p_match_literal(p):
    """match : STRING_LITERAL"""
    p[0] = LiteralMatch(_handle_literal_token(p[1]))


def p_match_regex(p):
    """match : REGEX"""
    regex_info = p[1].extras
    if 'unterminated' in regex_info and regex_info['unterminated']:
        raise RuleParseException.from_token(p[1], "Unterminated regex")

    flags = regex_info['flags'] if 'flags' in regex_info else set()
    p[0] = RegexMatch(regex_info['pattern'], flags)


def p_match_format(p):
    """match : FORMAT_SPEC"""
    specifier, width, leading_zeros = _handle_format_token(p[1])

    p[0] = FormatMatch(specifier, width, leading_zeros)


def p_match_insert_id(p):
    """match : OP_INSERT ID"""
    p[0] = InsertAliasMatch(p[2].text)


def p_match_insert_literal(p):
    """match : OP_INSERT STRING_LITERAL"""
    p[0] = InsertLiteralMatch(_handle_literal_token(p[2]))


def p_action_delete(p):
    """action : OP_DELETE"""
    p[0] = DeleteAction()


def p_action_save_to_alias(p):
    """action : OP_SAVE ID"""
    p[0] = SaveToAliasAction(p[2].text)


def p_action_replace_by_literal(p):
    """action : OP_XFORM STRING_LITERAL"""
    p[0] = ReplaceByLiteralAction(_handle_literal_token(p[2]))


def p_action_apply_function(p):
    """action : OP_XFORM ID"""
    p[0] = ApplyFunctionAction(p[2].text)


def p_action_reformat(p):
    """action : OP_XFORM FORMAT_SPEC"""
    specifier, width, leading_zeros = _handle_format_token(p[2])
    p[0] = ReformatAction(specifier, width, leading_zeros)


def _handle_literal_token(token):
    literal_info = token.extras
    if 'unterminated' in literal_info and literal_info['unterminated']:
        raise RuleParseException.from_token(token, "Unterminated string")
    if 'error' in literal_info:
        raise RuleParseException.from_token(token, literal_info['error'])

    return literal_info['value']


def _handle_format_token(token):
    spec_info = token.extras
    specifier = spec_info['specifier'] if 'specifier' in spec_info else None
    width = spec_info['width'] if 'width' in spec_info else None
    leading_zeros = spec_info['leading_zeros'] if 'leading_zeros' in spec_info else None

    if specifier is None:
        raise RuleParseException.from_token(token, "Missing format specifier")

    return specifier, width, leading_zeros


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
