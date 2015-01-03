# baon/core/plan/RmDirIfEmptyAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.plan.actions.RenamePlanAction import RenamePlanAction


class RmDirIfEmptyAction(RenamePlanAction):
    path = None
    
    def __init__(self, path):
        RenamePlanAction.__init__(self)
        self.path = path
    
    def _tuple_representation(self):
        return 'RmDirIfEmpty', self.path

    def execute(self):
        try:
            if os.path.isfile(self.path):
                raise RuntimeError("a file by that name exists")
            if not os.path.exists(self.path):
                raise RuntimeError("directory does not exist")
            
            is_empty = (len(os.listdir(self.path)) == 0)
            
            if not is_empty:
                return

            os.rmdir(self.path)
        except Exception as e:
            raise RuntimeError("Cannot remove '{0}': {1}".format(self.path, str(e)))
    
    def undo(self):
        try:
            if not os.path.exists(self.path):
                os.mkdir(self.path)
        except OSError:
            pass
