# logic/ast/matches/special/BetweenMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.matches.Match import Match


class BetweenMatch(Match):
    def __init__(self):
        Match.__init__(self)
    
    def execute(self, context):
        if context.next_unanchored:
            context.last_match_pos = context.position
        else:
            context.last_match_pos = None
            
        context.next_unanchored = True
        
        return ''

    def executeDelayed(self, text, context):
        for action in self.actions:
            text = action.execute(text, context)
            if text is False:
                break
        
        return text

    def _test_repr_node_name(self):
        return 'BETWEEN_MATCH'
