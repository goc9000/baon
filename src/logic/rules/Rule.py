# logic/rules/Rule.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.parsing.RulesASTNode import RulesASTNode


class Rule(RulesASTNode):
    alternatives = None
    
    def __init__(self):
        RulesASTNode.__init__(self)
        self.alternatives = []

    def isEmpty(self):
        return (len(self.alternatives) == 0) or all(alt.isEmpty() for alt in self.alternatives)

    def semanticCheck(self, scope):
        for alt in self.alternatives:
            alt.semanticCheck(scope)

    def execute(self, context):
        for alt in self.alternatives:
            matched = alt.execute(context)

            if matched is not False:
                return matched
        
        return False

    def test_repr(self):
        return ('RULE',) + tuple(alt.test_repr() for alt in self.alternatives)
