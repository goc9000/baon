# logic/ast/actions/Action.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.RulesASTNode import RulesASTNode


class Action(RulesASTNode):
    def __init__(self):
        RulesASTNode.__init__(self)

    def semanticCheck(self, scope):
        pass

    def execute(self, text, context):
        raise RuntimeError("execute() not implemented in subclass")
