# logic/matches/StartAnchorMatch.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from Match import Match


class StartAnchorMatch(Match):
    def __init__(self):
        Match.__init__(self)
    
    def _execute(self, context):
        if context.position == 0:
            context.last_match_pos = context.position
            context.next_unanchored = False
            return ''
        else:
            return False

    def _test_repr_impl(self):
        return 'START_ANCHOR_MATCH',
