# baon/logic/ast/actions/DeleteAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.actions.Action import Action


class DeleteAction(Action):
    def __init__(self):
        Action.__init__(self)

    def execute(self, context):
        return context._replace(matched_text=u'')
