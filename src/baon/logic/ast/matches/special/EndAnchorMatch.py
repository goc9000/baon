# baon/logic/ast/matches/special/EndAnchorMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.matches.MatchWithActions import MatchWithActions


class EndAnchorMatch(MatchWithActions):
    def __init__(self):
        MatchWithActions.__init__(self)
    
    def _execute_match_with_actions_impl(self, context):
        if context.next_unanchored or (context.position == len(context.text)):
            context.position = len(context.text)
            context.last_match_pos = len(context.text)
            context.next_unanchored = False
            return ''
        else:
            return False
