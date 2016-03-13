# baon/core/ast/matches/composite/SequenceMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.ASTNode import ast_node_children
from baon.core.ast.matches.Match import Match


class SequenceMatch(Match):
    terms = ast_node_children()

    def __init__(self, *terms):
        Match.__init__(self)
        self.terms = list(terms)

    def is_empty(self):
        return len(self.terms) == 0

    def execute(self, context):
        for solution in self._generate_solutions_rec(context, []):
            yield solution

    def _generate_solutions_rec(self, context, matches_so_far):
        term_index = len(matches_so_far)

        if term_index == len(self.terms):
            yield context._replace(matched_text=''.join(matches_so_far))
        else:
            for solution in self.terms[term_index].execute(context):
                for item in self._generate_solutions_rec(solution, matches_so_far + [solution.matched_text]):
                    yield item
