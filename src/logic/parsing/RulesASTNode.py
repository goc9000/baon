# logic/parsing/RulesASTToken.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


class RulesASTNode(object):
    def __init__(self):
        pass

    def test_repr(self):
        """The representation of this AST item in tests"""
        raise RuntimeError("test_repr() is not implemented in subclass")
