# logic/matches/special/RepeatMatch.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.matches.Match import Match


class RepeatMatch(Match):
    match = None
    at_least = None
    at_most = None
    
    def __init__(self, match, at_least, at_most):
        Match.__init__(self)
        
        self.match = match
        self.at_least = at_least
        self.at_most = at_most

    def _semanticCheck(self, scope):
        self.match.semanticCheck(scope)

    def _execute(self, context):
        committed = []
        
        match_pos = None
        
        while (self.at_most is None) or (len(committed) < self.at_most):
            old_position = context.position
            matched = self.match.execute(context)
            if matched is False:
                break
            if (match_pos is None) and (context.last_match_pos is not None):
                match_pos = context.last_match_pos
            
            committed.append(matched)
            
            if context.position == old_position:
                break
        
        if len(committed) < self.at_least:
            return False
        
        context.last_match_pos = match_pos
        
        return ''.join(committed)

    def _test_repr_impl(self):
        return 'REPEAT_MATCH', self.match.test_repr(), self.at_least, self.at_most
