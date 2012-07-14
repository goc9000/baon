# logic/matches/syn/InsertLiteralMatch.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from InsertionMatch import InsertionMatch

class InsertLiteralMatch(InsertionMatch):
    text = None
    
    def __init__(self, text):
        InsertionMatch.__init__(self)

        self.text = text
    
    def _execute(self, context):
        context.last_match_pos = None
        
        return self.text