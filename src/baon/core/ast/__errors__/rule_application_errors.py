# baon/core/ast/__errors__/rule_application_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta

from baon.core.errors.BAONError import BAONError


class RuleApplicationError(BAONError, metaclass=ABCMeta):
    scope = None


class AliasDependenciesTooComplexError(RuleApplicationError):
    def _get_format_string(self):
        return 'Dependencies of aliases are too complex'


class SpecifierExpectsNumberError(RuleApplicationError):
    def __init__(self, specifier, received):
        super(SpecifierExpectsNumberError, self).__init__(specifier=specifier, received=received)

    def _get_format_string(self):
        return "%{specifier} expects a number, received '{received}'"
