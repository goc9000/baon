# logic/matches/syn/InsertAliasMatch.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from InsertionMatch import InsertionMatch


class InsertAliasMatch(InsertionMatch):
    alias = None
    
    def __init__(self, alias):
        InsertionMatch.__init__(self)

        self.alias = alias
    
    def _execute(self, context):
        context.last_match_pos = None
        
        if self.alias in context.aliases:
            return context.aliases[self.alias]
        else:
            context.forward_aliases.add(self.alias)
            return ''

    def _test_repr_node_name(self):
        return 'INSERT_ALIAS_MATCH'

    def _test_repr_params(self):
        return self.alias,
