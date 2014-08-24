# logic/ast/matches/MatchWithActions.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.ASTNode import ast_node_children

from logic.ast.matches.Match import Match


class MatchWithActions(Match):
    actions = ast_node_children(order=100)

    def __init__(self):
        Match.__init__(self)
        self.actions = []

    def _execute_match_impl(self, context):
        text = self._execute_match_with_actions_impl(context)

        if text is not False:
            for action in self.actions:
                text = action.execute(text, context)
                if text is False:
                    break
        return text

    def _execute_match_with_actions_impl(self, context):
        raise RuntimeError("_execute_match_with_actions_impl() not implemented in subclass")
