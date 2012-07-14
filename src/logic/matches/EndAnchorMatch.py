# logic/matches/EndAnchorMatch.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from Match import Match

class EndAnchorMatch(Match):
    def __init__(self):
        Match.__init__(self)
    
    def _execute(self, context):
        if (context.next_unanchored) or (context.position == len(context.text)):
            context.position = len(context.text)
            context.last_match_pos = len(context.text)
            context.next_unanchored = False
            return ''
        else:
            return False
