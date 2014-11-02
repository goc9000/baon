# baon/core/ast/rule_application_exceptions.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONExceptionBase import BAONExceptionBase


class RuleApplicationException(BAONExceptionBase):
    scope = None

    def __init__(self, format_string, error_parameters):
        BAONExceptionBase.__init__(self, format_string, error_parameters)


class AliasDependenciesTooComplexException(RuleApplicationException):
    def __init__(self):
        RuleApplicationException.__init__(
            self, u"Dependencies of aliases are too complex", {})


class SpecifierExpectsNumberException(RuleApplicationException):
    def __init__(self, specifier, received):
        RuleApplicationException.__init__(
            self, u"%{specifier} expects a number, received '{received}'",
            {'specifier': specifier, 'received': received})
