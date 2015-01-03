# baon/core/plan/actions/MoveFileAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.plan.actions.RenamePlanAction import RenamePlanAction


class MoveFileAction(RenamePlanAction):
    from_path = None
    to_path = None
    
    def __init__(self, from_path, to_path):
        RenamePlanAction.__init__(self)
        self.from_path = from_path
        self.to_path = to_path
    
    def _tuple_representation(self):
        return 'MoveFile', self.from_path, self.to_path

    def execute(self):
        try:
            if not os.path.exists(self.from_path):
                raise RuntimeError("source does not exist")
            if os.path.exists(self.to_path):
                raise RuntimeError("destination already exists")
            
            os.rename(self.from_path, self.to_path)
        except Exception as e:
            raise RuntimeError("Cannot move '{0}' to '{1}': {2}".format(self.from_path, self.to_path, str(e)))
    
    def undo(self):
        try:
            if os.path.exists(self.to_path) and not os.path.exists(self.from_path):
                os.rename(self.to_path, self.from_path)
        except OSError:
            pass
