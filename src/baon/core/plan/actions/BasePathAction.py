# baon/core/plan/actions/BasePathAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.plan.actions.RenamePlanAction import RenamePlanAction


class BasePathAction(RenamePlanAction):
    path = None
    
    def __init__(self, plan, path):
        RenamePlanAction.__init__(self, plan)
        self.path = path
    
    def _tuple_representation(self):
        return 'BasePath', self.path
    
    def execute(self):
        if not os.path.exists(self.path):
            raise RuntimeError("Base path '{0}' does not exist".format(self.path))
    
    def undo(self):
        pass
