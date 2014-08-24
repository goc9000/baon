# logic/ast/actions/Action.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.ASTNode import ASTNode


class Action(ASTNode):
    def __init__(self):
        ASTNode.__init__(self)

    def execute(self, context):
        raise RuntimeError("execute() not implemented in subclass")
