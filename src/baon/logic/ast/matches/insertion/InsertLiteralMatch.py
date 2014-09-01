# baon/logic/ast/matches/insertion/InsertLiteralMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.matches.insertion.InsertionMatch import InsertionMatch
from baon.logic.ast.ASTNode import ast_node_field


class InsertLiteralMatch(InsertionMatch):
    text = ast_node_field()
    
    def __init__(self, text):
        InsertionMatch.__init__(self)

        self.text = text
    
    def _execute_match_with_actions_impl(self, context):
        context.last_match_pos = None
        
        return self.text
