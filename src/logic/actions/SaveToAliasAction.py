# logic/actions/SaveToAliasAction.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from Action import Action


class SaveToAliasAction(Action):
    alias = None
    
    def __init__(self, alias):
        Action.__init__(self)
        
        self.alias = alias
    
    def execute(self, text, context):
        context.aliases[self.alias] = text
        return text

    def _test_repr_node_name(self):
        return 'SAVE_ACTION'

    def _test_repr_params(self):
        return self.alias,
