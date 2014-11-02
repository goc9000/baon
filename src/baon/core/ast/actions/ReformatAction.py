# baon/core/ast/actions/ReformatAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import re

from baon.core.ast.actions.CompiledAction import CompiledAction, wrap_simple_text_function
from baon.core.ast.ASTNode import ast_node_field

from baon.core.ast.rule_application_exceptions import SpecifierExpectsNumberException

from baon.core.ast.rule_check_exceptions import UnrecognizedFormatSpecifierException,\
    WidthMustBeAtLeast1ForSpecifierException


def strip_zeroes(s):
    m = re.match(r'^(\s*)([0-9]+)(\s*)$', s)
    
    if m is None:
        raise SpecifierExpectsNumberException('d', s)
    
    mid = m.group(2).lstrip('0')
    if mid == '':
        mid = '0'
    
    return m.group(1) + mid + m.group(3)


def pad_with_zeroes(s, digits):
    m = re.match(r'^(\s*)([0-9]+)(\s*)$', s)
    
    if m is None:
        raise SpecifierExpectsNumberException('d', s)
    
    mid = m.group(2).lstrip('0')
    if mid == '':
        mid = '0'

    mid = mid.zfill(digits)

    return m.group(1) + mid + m.group(3)


class ReformatAction(CompiledAction):
    specifier = ast_node_field()
    width = ast_node_field()
    leading_zeros = ast_node_field(test_repr='leading')

    def __init__(self, specifier, width=None, leading_zeros=False):
        CompiledAction.__init__(self)

        self.specifier = specifier
        self.width = width
        self.leading_zeros = leading_zeros

    def _compile_function(self):
        if self.specifier == 'd':
            if self.width is None:
                return wrap_simple_text_function(strip_zeroes)
            if self.width <= 0:
                raise WidthMustBeAtLeast1ForSpecifierException(self.specifier)

            return wrap_simple_text_function(lambda text: pad_with_zeroes(text, self.width))

        raise UnrecognizedFormatSpecifierException(self.specifier)
