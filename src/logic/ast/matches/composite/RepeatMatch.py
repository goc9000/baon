# logic/ast/matches/composite/RepeatMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.errors.RuleCheckException import RuleCheckException

from logic.ast.matches.MatchWithActions import MatchWithActions
from logic.ast.ASTNode import ast_node_field, ast_node_child


class RepeatMatch(MatchWithActions):
    match = ast_node_child()
    at_least = ast_node_field(never_hide=True)
    at_most = ast_node_field(never_hide=True)
    
    def __init__(self, match, at_least, at_most):
        MatchWithActions.__init__(self)
        
        self.match = match
        self.at_least = at_least
        self.at_most = at_most

    def _semantic_check_before_children(self, scope):
        if self.at_least is None:
            raise RuleCheckException("Minimum number of matches must be specified")
        if self.at_least < 0:
            raise RuleCheckException("Minimum number of matches must be >= 0")

        if self.at_most is not None:
            if self.at_most < 1:
                raise RuleCheckException("Maximum number of matches must be >= 1")
            if self.at_least > self.at_most:
                raise RuleCheckException("Minimum number of matches must be >= the minimum")

    def _execute_match_with_actions_impl(self, context):
        committed = []
        
        match_pos = None
        
        while (self.at_most is None) or (len(committed) < self.at_most):
            old_position = context.position
            matched = self.match.execute(context)
            if matched is False:
                break
            if (match_pos is None) and (context.last_match_pos is not None):
                match_pos = context.last_match_pos
            
            committed.append(matched)
            
            if context.position == old_position:
                break
        
        if len(committed) < self.at_least:
            return False
        
        context.last_match_pos = match_pos
        
        return ''.join(committed)
