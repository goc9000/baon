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
    length = None
    message = None
    
    def __init__(self, message, line, column, length=None):
        self.message = message
        self.line = line
        self.column = column
        self.length = length
        
    def __str__(self):
        return self.message

    @staticmethod
    def from_token(token, message):
        return RuleParseException(message, token.lineno, token.colno, token.length)
