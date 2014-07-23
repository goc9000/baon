# logic/ast/RulesASTNodeChildRef.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


next_child_order = 0


class RulesASTNodeChildRef(object):
    name = None
    order = None

    def __init__(self, order=None):
        global next_child_order

        if order is not None:
            self.order = order
        else:
            self.order = next_child_order
        next_child_order += 1
