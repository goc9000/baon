# logic/actions/DeleteAction.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from Action import Action


class DeleteAction(Action):
    def __init__(self):
        Action.__init__(self)

    def execute(self, text, context):
        return ''

    def _test_repr_node_name(self):
        return 'DELETE_ACTION'
