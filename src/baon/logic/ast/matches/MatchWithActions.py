# baon/logic/ast/matches/MatchWithActions.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.ASTNode import ast_node_children

from baon.logic.ast.matches.Match import Match

from baon.logic.rules.MatchContext import MatchContext


class MatchWithActions(Match):
    actions = ast_node_children(order=100)

    def __init__(self):
        Match.__init__(self)
        self.actions = []

    def execute(self, context):
        for solution in self._execute_match_with_actions_impl(context):
            for action in self.actions:
                solution = action.execute(solution)

            yield solution

    def _execute_match_with_actions_impl(self, context):
        raise RuntimeError("_execute_match_with_actions_impl() not implemented in subclass")
