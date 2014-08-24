# logic/ast/matches/Match.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.ASTNode import ASTNode


class Match(ASTNode):

    def __init__(self):
        ASTNode.__init__(self)

    def execute(self, context):
        savept = context.save()
            
        text = self._execute_match_impl(context)
        
        if text is False:
            context.restore(savept)
            context.last_match_pos = None
        
        return text

    def _execute_match_impl(self, context):
        raise RuntimeError("_execute_match_impl() not implemented in subclass")
