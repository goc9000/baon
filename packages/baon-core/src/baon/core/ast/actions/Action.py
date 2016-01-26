# baon/core/ast/actions/Action.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta, abstractmethod

from baon.core.ast.ASTNode import ASTNode


class Action(ASTNode, metaclass=ABCMeta):
    def __init__(self):
        ASTNode.__init__(self)

    @abstractmethod
    def execute(self, context):
        return context
