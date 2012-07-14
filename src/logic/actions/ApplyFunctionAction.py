# logic/actions/ApplyFunctionAction.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from Action import Action
from logic.errors.RuleCheckException import RuleCheckException
from logic.grammar_utils import to_title_case

class ApplyFunctionAction(Action):
    fn = None
    error = None
    
    def __init__(self, fn_name):
        Action.__init__(self)
        
        if fn_name=="title":
            self.fn = lambda s,c: to_title_case(s)
        elif fn_name=="trim":
            self.fn = lambda s,c: s.strip()
        elif fn_name=="upper" or fn_name=="toupper":
            self.fn = lambda s,c: s.upper()
        elif fn_name=="lower" or fn_name=="tolower":
            self.fn = lambda s,c: s.lower()
        else:
            self.error = "Unsupported function '{0}'".format(fn_name)
    
    def semanticCheck(self, scope):
        Action.semanticCheck(self, scope)
        
        if not self.error is None:
            raise RuleCheckException(self.error, scope)

    def execute(self, text, context):
        return self.fn(text, context)
