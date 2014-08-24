# logic/ast/matches/composite/AlternativesMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.ASTNode import ast_node_children
from logic.ast.matches.MatchWithActions import MatchWithActions


class AlternativesMatch(MatchWithActions):
    alternatives = ast_node_children()
    
    def __init__(self):
        MatchWithActions.__init__(self)
        self.alternatives = []

    def is_empty(self):
        return (len(self.alternatives) == 0) or all(alt.is_empty() for alt in self.alternatives)

    def _execute_match_with_actions_impl(self, context):
        for alt in self.alternatives:
            matched = alt.execute(context)

            if matched is not False:
                return matched
        
        return False
