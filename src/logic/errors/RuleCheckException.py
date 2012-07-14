# logic/errors/RuleCheckException.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

class RuleCheckException(Exception):
    message = None
    scope = None
    
    def __init__(self, message, scope):
        self.message = message
        self.scope = scope
    
    def __str__(self):
        return self.message
