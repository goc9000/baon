# logic/ast/actions/ReformatAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import re

from logic.ast.actions.CompiledAction import CompiledAction
from logic.errors.RuleCheckException import RuleCheckException
from logic.errors.RuleApplicationException import RuleApplicationException


def strip_zeroes(s):
    m = re.match(r'(\s*)([0-9]+)(\s*)', s)
    
    if m is None:
        raise RuleApplicationException("%d applied to non-number")
    
    mid = m.group(2).lstrip('0')
    if mid == '':
        mid = '0'
    
    return m.group(1) + mid + m.group(3)


def pad_with_zeroes(s, digits):
    m = re.match(r'(\s*)([0-9]+)(\s*)', s)
    
    if m is None:
        raise RuleApplicationException("%Nd applied to non-number")
    
    mid = m.group(2).lstrip('0')
    if mid == '':
        mid = '0'

    mid = mid.zfill(digits)

    return m.group(1) + mid + m.group(3)


class ReformatAction(CompiledAction):
    specifier = None
    width = None
    leading_zeros = None

    def __init__(self, specifier, width=None, leading_zeros=False):
        CompiledAction.__init__(self)

        self.specifier = specifier
        self.width = width
        self.leading_zeros = leading_zeros

    def _compile_function(self):
        if self.specifier == 'd':
            if self.width is None:
                return lambda s, c: strip_zeroes(s)

            if self.width <= 0:
                raise RuleCheckException("Width must be >0 for specifier %d")

            return lambda s, c: pad_with_zeroes(s, self.width)

        raise RuleCheckException("Unrecognized format specifier '{0}'".format(self.specifier))

    def _test_repr_params(self):
        base_tuple = self.specifier,

        if self.width is not None:
            base_tuple += self.width,

        if self.leading_zeros is True:
            base_tuple += 'leading',

        return base_tuple
