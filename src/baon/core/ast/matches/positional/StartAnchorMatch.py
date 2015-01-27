# baon/core/ast/matches/positional/StartAnchorMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.MatchWithActions import MatchWithActions


class StartAnchorMatch(MatchWithActions):
    def __init__(self):
        MatchWithActions.__init__(self)
    
    def _execute_match_with_actions_impl(self, context):
        if context.position == 0:
            yield context._replace(matched_text='', anchored=True)
