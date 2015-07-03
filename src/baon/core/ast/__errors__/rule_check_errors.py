# baon/core/ast/__errors__/rule_check_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta

from baon.core.errors.BAONErrorWithSourceSpan import BAONErrorWithSourceSpan


class RuleCheckError(BAONErrorWithSourceSpan, metaclass=ABCMeta):
    scope = None
    
    def __init__(self, scope=None, source_span=None, **error_parameters):
        BAONErrorWithSourceSpan.__init__(self, source_span=source_span, **error_parameters)
        self.scope = scope


class ErrorInRegularExpressionError(RuleCheckError):
    def __init__(self):
        super().__init__()

    def _get_format_string(self):
        return 'Error in regular expression'


class InvalidRegexFlagError(RuleCheckError):
    def __init__(self, flag, scope=None, source_span=None):
        super().__init__(scope, source_span, flag=flag)

    def _get_format_string(self):
        return "Invalid regex flag '{flag}'"


class InvalidWidthForSpecifierError(RuleCheckError):
    def __init__(self, specifier, scope=None, source_span=None):
        super().__init__(scope, source_span, specifier=specifier)

    def _get_format_string(self):
        return "Invalid width for specifier '{specifier}'"


class Leading0sInapplicableToSpecifierError(RuleCheckError):
    def __init__(self, specifier, scope=None, source_span=None):
        super().__init__(scope, source_span, specifier=specifier)

    def _get_format_string(self):
        return "Leading 0s inapplicable to specifier '{specifier}'"


class MaximumMatchesZeroOrNegativeError(RuleCheckError):
    def __init__(self):
        super().__init__()

    def _get_format_string(self):
        return 'Maximum number of matches must be at least 1'


class MinimumMatchesGreaterThanMaximumError(RuleCheckError):
    def __init__(self):
        super().__init__()

    def _get_format_string(self):
        return 'Minimum number of matches must be greater than or equal to the minimum'


class MinimumMatchesNegativeError(RuleCheckError):
    def __init__(self):
        super().__init__()

    def _get_format_string(self):
        return 'Minimum number of matches must be non-negative'


class MinimumMatchesNotSpecifiedError(RuleCheckError):
    def __init__(self):
        super().__init__()

    def _get_format_string(self):
        return 'Minimum number of matches must be specified'


class UnrecognizedFormatSpecifierError(RuleCheckError):
    def __init__(self, specifier, scope=None, source_span=None):
        super().__init__(scope, source_span, specifier=specifier)

    def _get_format_string(self):
        return "Unrecognized format specifier '{specifier}'"


class UnsupportedFunctionError(RuleCheckError):
    def __init__(self, function_name, scope=None, source_span=None):
        super().__init__(scope, source_span, function_name=function_name)

    def _get_format_string(self):
        return "Unsupported function '{function_name}'"


class WidthInapplicableToSpecifierError(RuleCheckError):
    def __init__(self, specifier, scope=None, source_span=None):
        super().__init__(scope, source_span, specifier=specifier)

    def _get_format_string(self):
        return "Width inapplicable to specifier '{specifier}'"


class WidthMustBeAtLeast1ForSpecifierError(RuleCheckError):
    def __init__(self, specifier, scope=None, source_span=None):
        super().__init__(scope, source_span, specifier=specifier)

    def _get_format_string(self):
        return "Width must be at least 1 for specifier '{specifier}'"
