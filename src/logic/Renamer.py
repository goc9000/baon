import os

from FileRef import FileRef

class Renamer(object):
    ruleset = None
    use_ext = None
    use_path = None
    
    def __init__(self, ruleset, use_ext=False, use_path=False):
        self.ruleset = ruleset
        self.use_ext = use_ext
        self.use_path = use_path
        
    def rename(self, what):
        if isinstance(what, FileRef):
            return self._renameFile(what)
        
        return [self._renameFile(fref) for fref in what]
    
    def _renameFile(self, fref):
        try:
            fname = fref.filename
            
            if not self.use_path:
                path, fname = os.path.split(fname)
            if not self.use_ext:
                fname, ext = os.path.splitext(fname)
            
            fname = self.ruleset.applyOn(fname)
            
            if not self.use_ext:
                fname += ext
            if not self.use_path:
                fname = path + fname
            
            # todo: verify valid chars etc.
            
            return fref.renamed(fname)
        except Exception as e:
            return e
