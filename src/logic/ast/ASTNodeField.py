# logic/ast/ASTNodeField.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


next_field_order = 0


class ASTNodeField(object):
    name = None
    order = None
    default_value = None
    hide_for_value = None

    def __init__(self, default_value=None, test_repr=None, hide_for_value=None, never_hide=False, order=None):
        global next_field_order

        if order is not None:
            self.order = order
        else:
            self.order = next_field_order
        next_field_order += 1

        self.default_value = default_value
        self.test_repr = test_repr
        self.hide_for_value = hide_for_value
        if never_hide:
            self.hide_for_value = object()
