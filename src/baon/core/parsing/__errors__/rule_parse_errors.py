# baon/core/parsing/__errors__/rule_parse_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta

from baon.core.errors.BAONErrorWithSourceSpan import BAONErrorWithSourceSpan


class RuleParseError(BAONErrorWithSourceSpan, metaclass=ABCMeta):
    pass


class MissingFormatSpecifierError(RuleParseError):
    def __init__(self, source_span=None):
        super().__init__(source_span)

    def _get_format_string(self):
        return 'Missing format specifier'


class RuleSyntaxError(RuleParseError):
    def __init__(self, source_span=None):
        super().__init__(source_span)

    def _get_format_string(self):
        return 'Syntax error'


class StringLiteralNotQuotedProperlyError(RuleParseError):
    def __init__(self, source_span=None):
        super().__init__(source_span)

    def _get_format_string(self):
        return 'String literal not quoted properly'


class UnterminatedRegexError(RuleParseError):
    def __init__(self, source_span=None):
        super().__init__(source_span)

    def _get_format_string(self):
        return 'Unterminated regex'


class UnterminatedStringError(RuleParseError):
    def __init__(self, source_span=None):
        super().__init__(source_span)

    def _get_format_string(self):
        return 'Unterminated string'
