# logic/ast/matches/insertion/InsertLiteralMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.matches.insertion.InsertionMatch import InsertionMatch


class InsertLiteralMatch(InsertionMatch):
    text = None
    
    def __init__(self, text):
        InsertionMatch.__init__(self)

        self.text = text
    
    def _execute(self, context):
        context.last_match_pos = None
        
        return self.text

    def _test_repr_node_name(self):
        return 'INSERT_LITERAL_MATCH'

    def _test_repr_params(self):
        return self.text,
