from RenamePlanAction import RenamePlanAction

class MkDirIfNotExistsAction(RenamePlanAction):
    directory = None
    
    def __init__(self, plan, directory):
        RenamePlanAction.__init__(self, plan)
        self.directory = directory
    
    def _getRepr(self):
        return ('MkDirIfNotExists', self.directory)
