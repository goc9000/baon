# logic/matches/Match.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


class Match(object):
    actions = None

    def __init__(self):
        self.actions = []

    def semanticCheck(self, scope):
        self._semanticCheck(scope)
        
        for action in self.actions:
            action.semanticCheck(scope)
    
    def _semanticCheck(self, scope):
        pass

    def execute(self, context):
        savept = context.save()
            
        text = self._execute(context)

        if text is not False:
            for action in self.actions:
                text = action.execute(text, context)
                if text is False:
                    break
        
        if text is False:
            context.restore(savept)
            context.last_match_pos = None
        
        return text

