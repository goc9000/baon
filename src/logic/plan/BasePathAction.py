from RenamePlanAction import RenamePlanAction

import os

class BasePathAction(RenamePlanAction):
    path = None
    
    def __init__(self, plan, path):
        RenamePlanAction.__init__(self, plan)
        self.path = path
    
    def _getRepr(self):
        return ('BasePath', self.path)
    
    def execute(self):
        if not os.path.exists(self.path):
            raise RuntimeError("Base path '{0}' does not exist".format(self.path))
    
    def undo(self):
        pass
