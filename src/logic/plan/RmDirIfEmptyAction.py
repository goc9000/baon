from RenamePlanAction import RenamePlanAction

class RmDirIfEmptyAction(RenamePlanAction):
    directory = None
    
    def __init__(self, plan, directory):
        RenamePlanAction.__init__(self, plan)
        self.directory = directory
    
    def _getRepr(self):
        return ('RmDirIfEmpty', self.directory)
