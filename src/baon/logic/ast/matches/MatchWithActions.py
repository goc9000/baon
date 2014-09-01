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

    def _execute_match_impl(self, context):
        text = self._execute_match_with_actions_impl(context)

        if text is False:
            return

        action_context = MatchContext(
            text=context.text,
            position=context.position,
            aliases=context.aliases,
            matched_text=text
        )

        for action in self.actions:
            action_context = action.execute(action_context)
            if action_context is False:
                return False

        context.text = action_context.text
        context.position = action_context.position
        context.aliases = action_context.aliases

        return action_context.matched_text

    def _execute_match_with_actions_impl(self, context):
        raise RuntimeError("_execute_match_with_actions_impl() not implemented in subclass")
