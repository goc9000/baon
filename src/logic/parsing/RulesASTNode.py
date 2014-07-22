# logic/parsing/RulesASTToken.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.parsing.ItemWithPositionInSource import ItemWithPositionInSource


class RulesASTNode(ItemWithPositionInSource):
    def __init__(self):
        ItemWithPositionInSource.__init__(self)

    def test_repr(self):
        """The representation of this AST item in tests"""
        return\
            (self._test_repr_node_name(),) +\
            self._test_repr_params() +\
            tuple(child.test_repr() for child in self._test_repr_children())

    def _test_repr_node_name(self):
        raise RuntimeError("_test_repr_node_name() is not implemented in subclass")

    def _test_repr_params(self):
        return ()

    def _test_repr_children(self):
        return ()
