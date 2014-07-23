# logic/ast/matches/composite/SubRuleMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.matches.Match import Match
from logic.ast.ASTNode import ast_node_child


class SubRuleMatch(Match):
    rule = ast_node_child()
    
    def __init__(self, rule):
        Match.__init__(self)
        
        self.rule = rule

    def _semanticCheck(self, scope):
        self.rule.semanticCheck(scope)

    def _execute(self, context):
        return self.rule.execute(context)
