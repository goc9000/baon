# baon/core/parsing/__errors__/rule_parse_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONErrorWithSourceSpan import BAONErrorWithSourceSpan


class RuleParseError(BAONErrorWithSourceSpan):
    def __init__(self, format_string, error_parameters, source_span=None):
        BAONErrorWithSourceSpan.__init__(self, format_string, error_parameters, source_span)


class MissingFormatSpecifierError(RuleParseError):
    def __init__(self, source_span=None):
        RuleParseError.__init__(
            self, "Missing format specifier", {},
            source_span)


class RuleSyntaxError(RuleParseError):
    def __init__(self, source_span=None):
        RuleParseError.__init__(
            self, "Syntax error", {},
            source_span)


class StringLiteralNotQuotedProperlyError(RuleParseError):
    def __init__(self, source_span=None):
        RuleParseError.__init__(
            self, "String literal not quoted properly", {},
            source_span)


class UnterminatedRegexError(RuleParseError):
    def __init__(self, source_span=None):
        RuleParseError.__init__(
            self, "Unterminated regex", {},
            source_span)


class UnterminatedStringError(RuleParseError):
    def __init__(self, source_span=None):
        RuleParseError.__init__(
            self, "Unterminated string", {},
            source_span)
