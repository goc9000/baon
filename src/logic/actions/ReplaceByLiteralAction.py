# logic/actions/ReplaceByLiteralAction.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from Action import Action


class ReplaceByLiteralAction(Action):
    text = None
    
    def __init__(self, text):
        Action.__init__(self)

        self.text = text

    def execute(self, text, context):
        return self.text
