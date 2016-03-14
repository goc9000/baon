# baon/core/ast/matches/composite/MatchWithActions.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.ASTNode import ast_node_child, ast_node_children
from baon.core.ast.matches.Match import Match
from baon.core.rules.ActionContext import ActionContext


class MatchWithActions(Match):
    core_match = ast_node_child()
    actions = ast_node_children()

    def __init__(self, core_match, *actions):
        Match.__init__(self)
        self.core_match = core_match
        self.actions = list(actions)

    def add_action(self, action):
        self.actions.append(action)
        return self

    def execute(self, context):
        for solution in self.core_match.execute(context):

            action_context = ActionContext(text=solution.matched_text, aliases=solution.aliases)

            for action in self.actions:
                action_context = action.execute(action_context)

            yield solution._replace(matched_text=action_context.text, aliases=action_context.aliases)
