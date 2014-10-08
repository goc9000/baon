# baon/core/ast/matches/composite/RepeatMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.RuleCheckException import RuleCheckException

from baon.core.ast.matches.MatchWithActions import MatchWithActions
from baon.core.ast.ASTNode import ast_node_field, ast_node_child


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
        for solution in self._generate_solutions_rec(context, [], False):
            yield solution

    def _generate_solutions_rec(self, context, matches_so_far, must_advance_position):
        continuations_found = False

        if self.at_most is None or len(matches_so_far) < self.at_most:
            for solution in self.match.execute(context):
                if solution.position == context.position and must_advance_position:
                    continue

                continuations_found = True

                for item in self._generate_solutions_rec(
                        solution,
                        matches_so_far + [solution.matched_text],
                        self.at_most is None and solution.position == context.position
                ):
                    yield item

        if not continuations_found and len(matches_so_far) >= self.at_least:
            yield context._replace(matched_text=u''.join(matches_so_far))
