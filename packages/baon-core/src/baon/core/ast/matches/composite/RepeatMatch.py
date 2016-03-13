# baon/core/ast/matches/composite/RepeatMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.ASTNode import ast_node_field, ast_node_child
from baon.core.ast.__errors__.rule_check_errors import MinimumMatchesNotSpecifiedError, MinimumMatchesNegativeError, \
    MaximumMatchesZeroOrNegativeError, MinimumMatchesGreaterThanMaximumError
from baon.core.ast.matches.Match import Match


class RepeatMatch(Match):
    match = ast_node_child()
    at_least = ast_node_field(never_hide=True)
    at_most = ast_node_field(never_hide=True)
    
    def __init__(self, match, at_least, at_most):
        Match.__init__(self)
        
        self.match = match
        self.at_least = at_least
        self.at_most = at_most

    def _semantic_check_before_children(self, scope):
        if self.at_least is None:
            raise MinimumMatchesNotSpecifiedError()
        if self.at_least < 0:
            raise MinimumMatchesNegativeError()

        if self.at_most is not None:
            if self.at_most < 1:
                raise MaximumMatchesZeroOrNegativeError()
            if self.at_least > self.at_most:
                raise MinimumMatchesGreaterThanMaximumError()

    def execute(self, context):
        for solution in self._generate_solutions_rec(context, [], False):
            yield solution

    def _generate_solutions_rec(self, context, matches_so_far, must_advance_position):
        if self.at_most is None or len(matches_so_far) < self.at_most:
            for solution in self.match.execute(context):
                if solution.position == context.position and must_advance_position:
                    continue

                for item in self._generate_solutions_rec(
                        solution,
                        matches_so_far + [solution.matched_text],
                        self.at_most is None and solution.position == context.position
                ):
                    yield item

        if len(matches_so_far) >= self.at_least:
            yield context._replace(matched_text=''.join(matches_so_far))
