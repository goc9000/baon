# baon/core/plan/RenamePlanAction.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import re


PAT_FIRST_KW = re.compile(r'([\w]+)\s*')
PAT_QUOTED = re.compile(r'\s*("(\\"|[^"])*")\s*')


def quote_str(text):
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def unquote_str(text):
    return text[1:-1].replace('\\"', '"').replace("\\\\", "\\")


class RenamePlanAction(object):
    plan = None
    
    def __init__(self, plan):
        self.plan = plan
    
    def representation(self):
        tup = self._getRepr()
        kw = tup[0]
        args = tup[1:]
        
        if len(args) == 0:
            return kw
        else:
            return kw + ' ' + ' '.join(quote_str(arg) for arg in args)
    
    def _getRepr(self):
        raise RuntimeError('RenamePlanAction is abstract, has no _getRepr() implementation')
    
    def execute(self):
        raise RuntimeError('RenamePlanAction is abstract, has no execute() implementation')

    def undo(self):
        raise RuntimeError('RenamePlanAction is abstract, has no undo() implementation')

    @staticmethod
    def fromRepresentation(text, plan):
        m = PAT_FIRST_KW.match(text)
        if m is None:
            raise RuntimeError("Could not parse first keyword in line")
        
        kw = m.group(1)
        
        if kw not in ACTION_CLASSES_DICT:
            raise RuntimeError("Unknown action '{0}'".format(kw))
        
        cls, arg_count = ACTION_CLASSES_DICT[kw]
        
        pos = len(m.group(0))
        args = []
        for i in xrange(arg_count):
            m = PAT_QUOTED.match(text, pos)
            if m is None:
                raise RuntimeError("Could not parse argument #{0}/{1}".format(i+1, arg_count))
            
            args.append(unquote_str(m.group(1)))
            
            pos += len(m.group(0))
        
        if text[pos:].strip() != '':
            raise RuntimeError("Extra arguments found in line")
        
        return cls(plan, *args)

from BasePathAction import BasePathAction
from MkDirAction import MkDirAction
from MkDirIfNotExistsAction import MkDirIfNotExistsAction
from MoveFileAction import MoveFileAction
from RmDirAction import RmDirAction
from RmDirIfEmptyAction import RmDirIfEmptyAction

ACTION_CLASSES_DICT = {
    'BasePath':         (BasePathAction, 1),
    'MkDir':            (MkDirAction, 1),
    'MkDirIfNotExists': (MkDirIfNotExistsAction, 1),
    'MoveFile':         (MoveFileAction, 2),
    'RmDir':            (RmDirAction, 1),
    'RmDirIfEmpty':     (RmDirIfEmptyAction, 1)
}
