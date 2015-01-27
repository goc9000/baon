# baon/core/ast/rule_check_exceptions.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.ExceptionWithSourceSpan import ExceptionWithSourceSpan


class RuleCheckException(ExceptionWithSourceSpan):
    scope = None
    
    def __init__(self, format_string, error_parameters, scope=None, source_span=None):
        ExceptionWithSourceSpan.__init__(self, format_string, error_parameters, source_span)
        self.scope = scope


class ErrorInRegularExpressionException(RuleCheckException):
    def __init__(self, scope=None, source_span=None):
        RuleCheckException.__init__(
            self, "Error in regular expression", {},
            scope, source_span)


class InvalidRegexFlagException(RuleCheckException):
    def __init__(self, flag, scope=None, source_span=None):
        RuleCheckException.__init__(
            self, "Invalid regex flag '{flag}'",
            {'flag': flag},
            scope, source_span)


class InvalidWidthForSpecifierException(RuleCheckException):
    def __init__(self, specifier, scope=None, source_span=None):
        RuleCheckException.__init__(
            self, "Invalid width for specifier '{specifier}'",
            {'specifier': specifier},
            scope, source_span)


class Leading0sInapplicableToSpecifierException(RuleCheckException):
    def __init__(self, specifier, scope=None, source_span=None):
        RuleCheckException.__init__(
            self, "Leading 0s inapplicable to specifier '{specifier}'",
            {'specifier': specifier},
            scope, source_span)


class MaximumMatchesZeroOrNegativeException(RuleCheckException):
    def __init__(self, scope=None, source_span=None):
        RuleCheckException.__init__(
            self, "Maximum number of matches must be at least 1", {},
            scope, source_span)


class MinimumMatchesGreaterThanMaximumException(RuleCheckException):
    def __init__(self, scope=None, source_span=None):
        RuleCheckException.__init__(
            self, "Minimum number of matches must be greater than or equal to the minimum", {},
            scope, source_span)


class MinimumMatchesNegativeException(RuleCheckException):
    def __init__(self, scope=None, source_span=None):
        RuleCheckException.__init__(
            self, "Minimum number of matches must be non-negative", {},
            scope, source_span)


class MinimumMatchesNotSpecifiedException(RuleCheckException):
    def __init__(self, scope=None, source_span=None):
        RuleCheckException.__init__(
            self, "Minimum number of matches must be specified", {},
            scope, source_span)


class UnrecognizedFormatSpecifierException(RuleCheckException):
    def __init__(self, specifier, scope=None, source_span=None):
        RuleCheckException.__init__(
            self, "Unrecognized format specifier '{specifier}'",
            {'specifier': specifier},
            scope, source_span)


class UnsupportedFunctionException(RuleCheckException):
    def __init__(self, function_name, scope=None, source_span=None):
        RuleCheckException.__init__(
            self, "Unsupported function '{function_name}'",
            {'function_name': function_name},
            scope, source_span)


class WidthInapplicableToSpecifierException(RuleCheckException):
    def __init__(self, specifier, scope=None, source_span=None):
        RuleCheckException.__init__(
            self, "Width inapplicable to specifier '{specifier}'",
            {'specifier': specifier},
            scope, source_span)


class WidthMustBeAtLeast1ForSpecifierException(RuleCheckException):
    def __init__(self, specifier, scope=None, source_span=None):
        RuleCheckException.__init__(
            self, "Width must be at least 1 for specifier '{specifier}'",
            {'specifier': specifier},
            scope, source_span)
