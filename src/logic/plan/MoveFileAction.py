from RenamePlanAction import RenamePlanAction

class MoveFileAction(RenamePlanAction):
    from_path = None
    to_path = None
    
    def __init__(self, plan, from_path, to_path):
        RenamePlanAction.__init__(self, plan)
        self.from_path = from_path
        self.to_path = to_path
    
    def _getRepr(self):
        return ('MoveFile', self.from_path, self.to_path)
