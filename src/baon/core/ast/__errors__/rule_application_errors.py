# baon/core/ast/__errors__/rule_application_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONError import BAONError


class RuleApplicationError(BAONError):
    scope = None

    def __init__(self, format_string, error_parameters):
        BAONError.__init__(self, format_string, error_parameters)


class AliasDependenciesTooComplexError(RuleApplicationError):
    def __init__(self):
        RuleApplicationError.__init__(
            self, "Dependencies of aliases are too complex", {})


class SpecifierExpectsNumberError(RuleApplicationError):
    def __init__(self, specifier, received):
        RuleApplicationError.__init__(
            self, "%{specifier} expects a number, received '{received}'",
            {'specifier': specifier, 'received': received})
