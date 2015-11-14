# baon/core/parsing/parse_rules.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from ply import yacc
from ply.yacc import NullLogger

from baon.core.ast.actions.ApplyFunctionAction import ApplyFunctionAction
from baon.core.ast.actions.ApplyRuleSetAction import ApplyRuleSetAction
from baon.core.ast.actions.DeleteAction import DeleteAction
from baon.core.ast.actions.ReformatAction import ReformatAction
from baon.core.ast.actions.ReplaceByLiteralAction import ReplaceByLiteralAction
from baon.core.ast.actions.SaveToAliasAction import SaveToAliasAction
from baon.core.ast.matches.control.AlternativesMatch import AlternativesMatch
from baon.core.ast.matches.control.RepeatMatch import RepeatMatch
from baon.core.ast.matches.control.SequenceMatch import SequenceMatch
from baon.core.ast.matches.insertion.InsertAliasMatch import InsertAliasMatch
from baon.core.ast.matches.insertion.InsertLiteralMatch import InsertLiteralMatch
from baon.core.ast.matches.pattern.FormatMatch import FormatMatch
from baon.core.ast.matches.pattern.LiteralMatch import LiteralMatch
from baon.core.ast.matches.pattern.RegexMatch import RegexMatch
from baon.core.ast.matches.positional.EndAnchorMatch import EndAnchorMatch
from baon.core.ast.matches.positional.StartAnchorMatch import StartAnchorMatch
from baon.core.ast.matches.special.BetweenMatch import BetweenMatch
from baon.core.ast.matches.special.SearchReplaceMatch import SearchReplaceMatch
from baon.core.ast.rules.Rule import Rule
from baon.core.ast.rules.RuleSet import RuleSet
from baon.core.parsing.SourceSpan import SourceSpan
from baon.core.parsing.__errors__.rule_parse_errors import MissingFormatSpecifierError, UnterminatedStringError, \
    UnterminatedRegexError, RuleSyntaxError
from baon.core.parsing.tokenize_rules import tokenize_rules, tokens


# Ensure tokens is not seen as unused and removed by the IDE
assert len(tokens) > 0


class EOFRuleParseException(BaseException):
    def __init__(self):
        BaseException.__init__(self)


def p_rule_set_add_rule(p):
    """rule_set : rule_set RULE_SEP rule"""
    p[0] = p[1]
    if not p[3].is_empty():
        p[0].add_rule(p[3])

    _set_source_span(p[0], p[1], p[3])


def p_rule_set_base(p):
    """rule_set : rule"""
    p[0] = RuleSet()
    if not p[1].is_empty():
        p[0].add_rule(p[1])

    _set_source_span(p[0], p[1])


def p_rule(p):
    """rule : alternatives_match"""
    p[0] = Rule(p[1])
    _set_source_span(p[0], p[1])


def p_alternatives_match_add_sequence_match(p):
    """alternatives_match : alternatives_match OP_OR sequence_match"""
    p[0] = p[1]
    p[0].add_alternative(p[3])
    _set_source_span(p[0], p[1], p[3])


def p_alternatives_match_base(p):
    """alternatives_match : sequence_match"""
    p[0] = AlternativesMatch()
    p[0].add_alternative(p[1])
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
    p[0].add_action(p[2])
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
        raise UnterminatedRegexError(p[1].source_span)

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

    raise RuleSyntaxError(token.source_span)


def _set_source_span(node, from_item, to_item=None):
    if to_item is None:
        node.source_span = SourceSpan.copy(from_item.source_span)
    else:
        node.source_span = SourceSpan.from_to(from_item.source_span, to_item.source_span)


def _handle_literal_token(token):
    literal_info = token.extras
    if 'unterminated' in literal_info and literal_info['unterminated']:
        raise UnterminatedStringError(token.source_span)
    if 'error' in literal_info:
        error = literal_info['error']
        error.source_span = token.source_span
        raise error

    return literal_info['value']


def _handle_format_token(token):
    spec_info = token.extras
    specifier = spec_info['specifier'] if 'specifier' in spec_info else None
    width = spec_info['width'] if 'width' in spec_info else None
    leading_zeros = spec_info['leading_zeros'] if 'leading_zeros' in spec_info else None

    if specifier is None:
        raise MissingFormatSpecifierError(token.source_span)

    return specifier, width, leading_zeros


start = 'rule_set'

parser_template = yacc.yacc(write_tables=False, debug=False, errorlog=NullLogger())


class RulesLexerForYACC(object):
    _token_stream = None

    def __init__(self):
        pass

    def input(self, rules_text):
        self._token_stream = tokenize_rules(rules_text)

    def token(self):
        return next(self._token_stream, None)


def parse_rules(rules_text, start_rule=None):
    if start_rule is None:
        parser = parser_template
    else:
        parser = yacc.yacc(start=start_rule, debug=False, write_tables=False, errorlog=NullLogger())

    try:
        return parser.parse(rules_text, RulesLexerForYACC())
    except EOFRuleParseException:
        raise RuleSyntaxError(source_span=SourceSpan.at_end_of_source(rules_text)) from None
