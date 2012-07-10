from RenamePlanAction import RenamePlanAction

class BasePathAction(RenamePlanAction):
    path = None
    
    def __init__(self, plan, path):
        RenamePlanAction.__init__(self, plan)
        self.path = path
    
    def _getRepr(self):
        return ('BasePath', self.path)
