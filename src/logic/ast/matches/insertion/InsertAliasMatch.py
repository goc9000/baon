# logic/ast/matches/insertion/InsertAliasMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.matches.insertion.InsertionMatch import InsertionMatch
from logic.ast.ASTNode import ast_node_field


class InsertAliasMatch(InsertionMatch):
    alias = ast_node_field()
    
    def __init__(self, alias):
        InsertionMatch.__init__(self)

        self.alias = alias
    
    def _execute_match_with_actions_impl(self, context):
        context.last_match_pos = None
        return context.aliases[self.alias]
