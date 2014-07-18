# logic/parsing/RulesLexer.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from ply import lex
from ply.lex import TOKEN

from logic.lang_utils import is_dictish
from logic.baon_utils import decode_baon_string_literal
from logic.parsing.RulesToken import RulesToken


class RulesLexer(object):
    """
    Design notes: The lexer is designed to be very lenient, in order for it to be used by the rules syntax highlighter.
    As a result, it may emit tokens that are not entirely syntactically correct, e.g. unterminated string literals or
    incomplete format specifiers. The parser has to account for this when receiving the tokens.
    """
    _lexer = None

    def __init__(self):
        self._lexer = lex.lex(module=self)
        pass
    
    def parse(self, rules_text):
        return (lex_token.value for lex_token in self.parse_lex_tokens(rules_text))

    def parse_lex_tokens(self, rules_text):
        self._lexer.input(rules_text)
        self._lexer.lineno = (1, 0)
        return self.augment_lex_tokens(self.merge_error_tokens(self._lexer))

    @staticmethod
    def merge_error_tokens(lex_tokens_stream):
        last_err_token = None

        for lex_token in lex_tokens_stream:
            if lex_token.type == 'error':
                if last_err_token is not None:
                    if last_err_token.lexpos + len(last_err_token.value) == lex_token.lexpos:
                        last_err_token.value += lex_token.value
                        continue

                    yield last_err_token

                last_err_token = lex_token
            else:
                if last_err_token is not None:
                    yield last_err_token
                    last_err_token = None

                yield lex_token

        if last_err_token is not None:
            yield last_err_token

    @staticmethod
    def augment_lex_tokens(lex_tokens_stream):
        for lex_token in lex_tokens_stream:
            token = RulesToken()
            token.type = lex_token.type
            token.text = lex_token.value
            token.lexpos = lex_token.lexpos
            token.lineno = lex_token.lineno[0]
            token.colno = 1 + lex_token.lexpos - lex_token.lineno[1]

            if is_dictish(lex_token.value):
                for k, v in lex_token.value.items():
                    if k == 'text':
                        token.text = v
                    else:
                        if token.value is None:
                            token.value = {}

                        token.value[k] = v

            lex_token.value = token

            yield lex_token

    tokens = (
        'PARA_OPEN',
        'PARA_CLOSE',
        'RULE_SEP',
        'OP_OR',
        'OP_DELETE',
        'OP_XFORM',
        'OP_SAVE',
        'OP_INSERT',
        'OP_SEARCH',
        'OP_REPEAT',
        'BETWEEN',
        'ANCHOR_START',
        'ANCHOR_END',
        'FORMAT_SPEC',
        'STRING_LITERAL',
        'REGEX',
        'ID',
    )

    t_PARA_OPEN = r'\('
    t_PARA_CLOSE = r'\)'

    t_RULE_SEP = r';'  # Also newline, but this is handled separately

    t_OP_OR = r'\|'

    t_OP_DELETE = r'!'
    t_OP_XFORM = r'->'
    t_OP_SAVE = r'>>'

    t_OP_INSERT = r'<<'
    t_OP_SEARCH = r'@'

    t_BETWEEN = r'\.\.'
    t_ANCHOR_START = r'\^'
    t_ANCHOR_END = r'\$'

    t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    t_ignore = ' \t'

    @TOKEN(r'%(?P<fmt_width>[0-9]*)(?P<fmt_spec>[a-zA-Z]*)')
    def t_FORMAT_SPEC(self, t):
        specifier = t.lexer.lexmatch.group('fmt_spec')

        t.value = {
            'text': t.value,
            'specifier': specifier if specifier != '' else None,
        }

        width = t.lexer.lexmatch.group('fmt_width')
        if width != '':
            t.value['width'] = int(width)
            if width.startswith('0') and len(width) > 1:
                t.value['leading_zeros'] = True

        return t

    @TOKEN('"([^"\\n\\\\]|\\\\[^\\n]?)*(?P<end_dquote>"?)|\'([^\'\\n\\\\]|\\\\[^\\n]?)*(?P<end_quote>\'?)')
    def t_STRING_LITERAL(self, t):
        t.value = {
            'text': t.value,
        }

        last_quote_group = 'end_dquote' if t.value['text'][0] == '"' else 'end_quote'

        if t.lexer.lexmatch.group(last_quote_group) != t.value['text'][0]:
            t.value['unterminated'] = True
        else:
            try:
                t.value['value'] = decode_baon_string_literal(t.value['text'])
            except:
                pass

        return t

    @TOKEN('/(?P<regex_body>([^/\\n]|//)*)(?P<end_regex>(/[a-zA-Z]*)?)')
    def t_REGEX(self, t):
        t.value = {
            'text': t.value,
        }

        if t.lexer.lexmatch.group('end_regex') == '':
            t.value['unterminated'] = True
        else:
            t.value['pattern'] = t.lexer.lexmatch.group('regex_body').replace(u'//', u'/')
            t.value['flags'] = set(t.lexer.lexmatch.group('end_regex')[1:])

        return t

    @TOKEN('\?|\*|\+')
    def t_OP_REPEAT(self, t):
        t.value = {
            'text': t.value,
            'min': 1 if t.value == '+' else 0,
            'max': 1 if t.value == '?' else None,
        }

        return t

    @TOKEN('\\n')
    def t_newline(self, t):
        t.type = 'RULE_SEP'
        t.lexer.lineno = t.lexer.lineno[0] + 1, t.lexpos + 1
        return t

    def t_error(self, t):
        t.value = t.value[0]
        t.lexer.skip(1)
        return t
