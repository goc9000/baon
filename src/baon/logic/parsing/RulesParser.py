# baon/logic/parsing/RulesParser.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from ply import yacc
from ply.yacc import NullLogger

from baon.logic.ast.rules.RuleSet import RuleSet
from baon.logic.ast.rules.Rule import Rule

from baon.logic.ast.matches.composite.AlternativesMatch import AlternativesMatch
from baon.logic.ast.matches.composite.SequenceMatch import SequenceMatch
from baon.logic.ast.matches.composite.RepeatMatch import RepeatMatch
from baon.logic.ast.matches.composite.SearchReplaceMatch import SearchReplaceMatch

from baon.logic.ast.matches.special.StartAnchorMatch import StartAnchorMatch
from baon.logic.ast.matches.special.EndAnchorMatch import EndAnchorMatch
from baon.logic.ast.matches.special.BetweenMatch import BetweenMatch

from baon.logic.ast.matches.pattern.LiteralMatch import LiteralMatch
from baon.logic.ast.matches.pattern.RegexMatch import RegexMatch
from baon.logic.ast.matches.pattern.FormatMatch import FormatMatch

from baon.logic.ast.matches.insertion.InsertLiteralMatch import InsertLiteralMatch
from baon.logic.ast.matches.insertion.InsertAliasMatch import InsertAliasMatch

from baon.logic.ast.actions.DeleteAction import DeleteAction
from baon.logic.ast.actions.SaveToAliasAction import SaveToAliasAction
from baon.logic.ast.actions.ReplaceByLiteralAction import ReplaceByLiteralAction
from baon.logic.ast.actions.ApplyFunctionAction import ApplyFunctionAction
from baon.logic.ast.actions.ReformatAction import ReformatAction
from baon.logic.ast.actions.ApplyRuleSetAction import ApplyRuleSetAction

from baon.logic.errors.RuleParseException import RuleParseException

from baon.logic.parsing.RulesLexer import RulesLexer, tokens
from baon.logic.parsing.SourceSpan import SourceSpan


class EOFRuleParseException:
    def __init__(self):
        pass


def p_rule_set_add_rule(p):
    """rule_set : rule_set RULE_SEP rule"""
    p[0] = p[1]
    if not p[3].is_empty():
        p[0].rules.append(p[3])

    _set_source_span(p[0], p[1], p[3])


def p_rule_set_base(p):
    """rule_set : rule"""
    p[0] = RuleSet()
    if not p[1].is_empty():
        p[0].rules.append(p[1])

    _set_source_span(p[0], p[1])


def p_rule(p):
    """rule : alternatives_match"""
    p[0] = Rule(p[1])
    _set_source_span(p[0], p[1])


def p_alternatives_match_add_sequence_match(p):
    """alternatives_match : alternatives_match OP_OR sequence_match"""
    p[0] = p[1]
    p[0].alternatives.append(p[3])
    _set_source_span(p[0], p[1], p[3])


def p_alternatives_match_base(p):
    """alternatives_match : sequence_match"""
    p[0] = AlternativesMatch()
    p[0].alternatives.append(p[1])
    _set_source_span(p[0], p[1])


def p_sequence_match_add_term(p):
    """sequence_match : sequence_match sequence_match_term"""
    p[0] = p[1]
    p[0].terms.append(p[2])
    _set_source_span(p[0], p[1], p[2])


def p_sequence_match_empty(p):
    """sequence_match : """
    p[0] = SequenceMatch()

    try:
        p[0].source_span = SourceSpan.right_after(p[-1].source_span)
    except AttributeError:
        p[0].source_span = SourceSpan.at_beginning()


def p_match_term_match(p):
    """sequence_match_term : match"""
    p[0] = p[1]


def p_match_term_search(p):
    """sequence_match_term : OP_SEARCH match"""
    p[0] = SearchReplaceMatch(p[2])
    _set_source_span(p[0], p[1], p[2])


def p_match_add_actions(p):
    """match : match action"""
    p[0] = p[1]
    p[0].actions.append(p[2])
    _set_source_span(p[0], p[1], p[2])


def p_match_add_repeat(p):
    """match : match OP_REPEAT"""
    p[0] = RepeatMatch(p[1], p[2].extras['min'], p[2].extras['max'])
    _set_source_span(p[0], p[1], p[2])


def p_match_anchor_start(p):
    """match : ANCHOR_START"""
    p[0] = StartAnchorMatch()
    _set_source_span(p[0], p[1])


def p_match_anchor_end(p):
    """match : ANCHOR_END"""
    p[0] = EndAnchorMatch()
    _set_source_span(p[0], p[1])


def p_match_between(p):
    """match : BETWEEN"""
    p[0] = BetweenMatch()
    _set_source_span(p[0], p[1])


def p_match_literal(p):
    """match : STRING_LITERAL"""
    p[0] = LiteralMatch(_handle_literal_token(p[1]))
    _set_source_span(p[0], p[1])


def p_match_regex(p):
    """match : REGEX"""
    regex_info = p[1].extras
    if 'unterminated' in regex_info and regex_info['unterminated']:
        raise RuleParseException("Unterminated regex", p[1].source_span)

    flags = regex_info['flags'] if 'flags' in regex_info else set()
    p[0] = RegexMatch(regex_info['pattern'], flags)
    _set_source_span(p[0], p[1])


def p_match_format(p):
    """match : FORMAT_SPEC"""
    specifier, width, leading_zeros = _handle_format_token(p[1])

    p[0] = FormatMatch(specifier, width, leading_zeros)
    _set_source_span(p[0], p[1])


def p_match_insert_id(p):
    """match : OP_INSERT ID"""
    p[0] = InsertAliasMatch(p[2].text)
    _set_source_span(p[0], p[1], p[2])


def p_match_subrule(p):
    """match : PARA_OPEN alternatives_match PARA_CLOSE"""
    p[0] = p[2]
    _set_source_span(p[0], p[1], p[3])


def p_match_insert_literal(p):
    """match : OP_INSERT STRING_LITERAL"""
    p[0] = InsertLiteralMatch(_handle_literal_token(p[2]))
    _set_source_span(p[0], p[1], p[2])


def p_action_delete(p):
    """action : OP_DELETE"""
    p[0] = DeleteAction()
    _set_source_span(p[0], p[1])


def p_action_save_to_alias(p):
    """action : OP_SAVE ID"""
    p[0] = SaveToAliasAction(p[2].text)
    _set_source_span(p[0], p[1], p[2])


def p_action_replace_by_literal(p):
    """action : OP_XFORM STRING_LITERAL"""
    p[0] = ReplaceByLiteralAction(_handle_literal_token(p[2]))
    _set_source_span(p[0], p[1], p[2])


def p_action_apply_function(p):
    """action : OP_XFORM ID"""
    p[0] = ApplyFunctionAction(p[2].text)
    _set_source_span(p[0], p[1], p[2])

def p_action_reformat(p):
    """action : OP_XFORM FORMAT_SPEC"""
    specifier, width, leading_zeros = _handle_format_token(p[2])
    p[0] = ReformatAction(specifier, width, leading_zeros)
    _set_source_span(p[0], p[1], p[2])


def p_action_apply_sub_rule(p):
    """action : OP_XFORM PARA_OPEN rule_set PARA_CLOSE"""
    p[0] = ApplyRuleSetAction(p[3])
    _set_source_span(p[0], p[1], p[4])


def p_error(token):
    if token is None:
        raise EOFRuleParseException

    raise RuleParseException("Syntax error", token.source_span)


def _set_source_span(node, from_item, to_item=None):
    if to_item is None:
        node.source_span = SourceSpan.copy(from_item.source_span)
    else:
        node.source_span = SourceSpan.from_to(from_item.source_span, to_item.source_span)


def _handle_literal_token(token):
    literal_info = token.extras
    if 'unterminated' in literal_info and literal_info['unterminated']:
        raise RuleParseException("Unterminated string", token.source_span)
    if 'error' in literal_info:
        raise RuleParseException(literal_info['error'], token.source_span)

    return literal_info['value']


def _handle_format_token(token):
    spec_info = token.extras
    specifier = spec_info['specifier'] if 'specifier' in spec_info else None
    width = spec_info['width'] if 'width' in spec_info else None
    leading_zeros = spec_info['leading_zeros'] if 'leading_zeros' in spec_info else None

    if specifier is None:
        raise RuleParseException("Missing format specifier", token.source_span)

    return specifier, width, leading_zeros


start = 'rule_set'

parser_template = yacc.yacc(write_tables=False, debug=False, errorlog=NullLogger())


class RulesParser(object):
    @staticmethod
    def parse(rules_text):
        return RulesParser._run_parser(parser_template, rules_text)

    @staticmethod
    def debug_parse(rules_text, start_rule):
        parser = yacc.yacc(start=start_rule, debug=False, write_tables=False, errorlog=NullLogger())
        return RulesParser._run_parser(parser, rules_text)

    @staticmethod
    def _run_parser(parser, rules_text):
        try:
            return parser.parse(rules_text, RulesLexerForYACC())
        except EOFRuleParseException:
            exception = RuleParseException('Syntax error')
            exception.source_span = SourceSpan.at_end_of_source(rules_text)
            raise exception


class RulesLexerForYACC(object):
    _token_stream = None

    def __init__(self):
        pass

    def input(self, rules_text):
        self._token_stream = RulesLexer.tokenize(rules_text)

    def token(self):
        return next(self._token_stream, None)