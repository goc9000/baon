# logic/errors/RuleParseException.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


class RuleParseException(Exception):
    line = None
    column = None
    message = None
    
    def __init__(self, message, line, col):
        self.message = message
        self.line = line
        self.column = col
        
    def __str__(self):
        return self.message
