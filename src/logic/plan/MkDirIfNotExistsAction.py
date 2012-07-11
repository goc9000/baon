from RenamePlanAction import RenamePlanAction

import os

class MkDirIfNotExistsAction(RenamePlanAction):
    directory = None
    
    def __init__(self, plan, directory):
        RenamePlanAction.__init__(self, plan)
        self.directory = directory
    
    def _getRepr(self):
        return ('MkDirIfNotExists', self.directory)

    def execute(self):
        path = os.path.join(self.plan.base_path, self.directory)
        
        try:
            if os.path.isfile(path):
                raise RuntimeError("a file by that name already exists")
            if os.path.exists(path):
                return
                
            os.mkdir(path)
        except Exception as e:
            raise RuntimeError("Cannot create '{0}': {1}".format(path, str(e)))
    
    def undo(self):
        path = os.path.join(self.plan.base_path, self.directory)
        
        try:
            if len(os.listdir(path)) == 0:
                os.rmdir(path)
        except:
            pass
