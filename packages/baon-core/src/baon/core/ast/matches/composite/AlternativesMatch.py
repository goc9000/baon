# baon/core/ast/matches/composite/AlternativesMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.ASTNode import ast_node_children
from baon.core.ast.matches.Match import Match


class AlternativesMatch(Match):
    alternatives = ast_node_children()
    
    def __init__(self, *alternatives):
        Match.__init__(self)
        self.alternatives = list(alternatives)

    def is_empty(self):
        return (len(self.alternatives) == 0) or all(alt.is_empty() for alt in self.alternatives)

    def add_alternative(self, alternative):
        self.alternatives.append(alternative)
        return self

    def execute(self, context):
        for alternative in self.alternatives:
            for solution in alternative.execute(context):
                yield solution
