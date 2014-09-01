# baon/logic/plan/MoveFileAction.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.logic.plan.RenamePlanAction import RenamePlanAction


class MoveFileAction(RenamePlanAction):
    from_path = None
    to_path = None
    
    def __init__(self, plan, from_path, to_path):
        RenamePlanAction.__init__(self, plan)
        self.from_path = from_path
        self.to_path = to_path
    
    def _getRepr(self):
        return 'MoveFile', self.from_path, self.to_path

    def execute(self):
        path1 = os.path.join(self.plan.base_path, self.from_path)
        path2 = os.path.join(self.plan.base_path, self.to_path)
        
        try:
            if not os.path.exists(path1):
                raise RuntimeError("source does not exist")
            if os.path.exists(path2):
                raise RuntimeError("destination already exists")
            
            os.rename(path1, path2)
        except Exception as e:
            raise RuntimeError("Cannot move '{0}' to '{1}': {2}".format(path1, path2, str(e)))
    
    def undo(self):
        path1 = os.path.join(self.plan.base_path, self.from_path)
        path2 = os.path.join(self.plan.base_path, self.to_path)
        
        try:
            if os.path.exists(path2) and not os.path.exists(path1):
                os.rename(path2, path1)
        except OSError:
            pass
