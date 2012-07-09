import os

class RenamePlan(object):
    base_path = None
    steps = None
    
    def __init__(self, base_path, files):
        self.base_path = base_path
        self.steps = []

        if (files is None) or (len(files) == 0) or not (any(ren.changed() for ren in files)):
            raise RuntimeError("Nothing to do!")
        if any(ren.error is not None for ren in files):
            raise RuntimeError("There are unresolved errors in the renamed files list")
        
        print self._getNeedToCreateDirs(files)
        
        raise RuntimeError("PAF")
    
    def _getNeedToCreateDirs(self, files):
        dirs = set()
        
        for f in files:
            for p in self._allParents(f.filename):
                dirs.add(p)
        
        dirs2 = []
        
        for d in dirs:
            path = os.path.join(self.base_path, d)
            if not os.path.exists(path):
                dirs2.append(d)
            else:
                if not os.path.isdir(path):
                    raise RuntimeError("Need to create directory '{0}', but there's a file with the same name".format(d))
        
        dirs2.sort()
        
        return dirs2
    
    def _getNeedToDeleteDirs(self, dirs):
        pass
    
    def _allParents(self, filename):
        base = ''
        
        path, _ = os.path.split(filename)
        
        if path != '':
            for comp in path.split(os.sep):
                base = os.path.join(base, comp)
                yield base
