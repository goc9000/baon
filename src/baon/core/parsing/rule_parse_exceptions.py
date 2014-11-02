# baon/core/parsing/rule_parse_exceptions.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.ExceptionWithSourceSpan import ExceptionWithSourceSpan


class RuleParseException(ExceptionWithSourceSpan):
    def __init__(self, format_string, error_parameters, source_span=None):
        ExceptionWithSourceSpan.__init__(self, format_string, error_parameters, source_span)


class MissingFormatSpecifierException(RuleParseException):
    def __init__(self, source_span=None):
        RuleParseException.__init__(
            self, u"Missing format specifier", {},
            source_span)


class RuleSyntaxErrorException(RuleParseException):
    def __init__(self, source_span=None):
        RuleParseException.__init__(
            self, u"Syntax error", {},
            source_span)


class StringLiteralNotQuotedProperlyException(RuleParseException):
    def __init__(self, source_span=None):
        RuleParseException.__init__(
            self, u"String literal not quoted properly", {},
            source_span)


class UnterminatedRegexException(RuleParseException):
    def __init__(self, source_span=None):
        RuleParseException.__init__(
            self, u"Unterminated regex", {},
            source_span)


class UnterminatedStringException(RuleParseException):
    def __init__(self, source_span=None):
        RuleParseException.__init__(
            self, u"Unterminated string", {},
            source_span)
