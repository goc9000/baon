# baon/core/plan/actions/MkDirIfNotExistsAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.plan.actions.RenamePlanAction import RenamePlanAction


class MkDirIfNotExistsAction(RenamePlanAction):
    path = None
    
    def __init__(self, path):
        RenamePlanAction.__init__(self)
        self.path = path
    
    def _tuple_representation(self):
        return 'MkDirIfNotExists', self.path

    def execute(self):
        try:
            if os.path.isfile(self.path):
                raise RuntimeError("a file by that name already exists")
            if os.path.exists(self.path):
                return
                
            os.mkdir(self.path)
        except Exception as e:
            raise RuntimeError("Cannot create '{0}': {1}".format(self.path, str(e)))
    
    def undo(self):
        try:
            if len(os.listdir(self.path)) == 0:
                os.rmdir(self.path)
        except OSError:
            pass
