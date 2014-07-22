# logic/matches/special/SubRuleMatch.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.matches.Match import Match


class SubRuleMatch(Match):
    rule = None
    
    def __init__(self, rule):
        Match.__init__(self)
        
        self.rule = rule

    def _semanticCheck(self, scope):
        self.rule.semanticCheck(scope)

    def _execute(self, context):
        return self.rule.execute(context)

    def _test_repr_node_name(self):
        return 'SUBRULE_MATCH'

    def _test_repr_children_impl(self):
        return self.rule,
