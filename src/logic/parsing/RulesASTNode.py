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
        raise RuntimeError("test_repr() is not implemented in subclass")
