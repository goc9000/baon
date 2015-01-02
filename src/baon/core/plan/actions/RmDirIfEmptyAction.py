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
    directory = None
    
    def __init__(self, plan, directory):
        RenamePlanAction.__init__(self, plan)
        self.directory = directory
    
    def _getRepr(self):
        return 'RmDirIfEmpty', self.directory

    def execute(self):
        path = os.path.join(self.plan.base_path, self.directory)
        
        try:
            if os.path.isfile(path):
                raise RuntimeError("a file by that name exists")
            if not os.path.exists(path):
                raise RuntimeError("directory does not exist")
            
            is_empty = (len(os.listdir(path)) == 0)
            
            if not is_empty:
                return
                
            os.rmdir(path)
        except Exception as e:
            raise RuntimeError("Cannot remove '{0}': {1}".format(path, str(e)))
    
    def undo(self):
        path = os.path.join(self.plan.base_path, self.directory)
        
        try:
            if not os.path.exists(path):
                os.mkdir(path)
        except OSError:
            pass
