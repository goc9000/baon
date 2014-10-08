# baon/core/errors/RuleApplicationException.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


class RuleApplicationException(Exception):
    message = None
    
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message
