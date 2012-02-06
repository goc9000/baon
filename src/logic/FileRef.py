import os

class FileRef(object):
    fullPath = None
    filename = None
    isDir = None
    
    def __init__(self, fullPath, filename, isDir = None):
        self.fullPath = fullPath
        self.filename = filename
        if isDir is None:
            isDir = os.path.isdir(fullPath)
        self.isDir = isDir

    def __cmp__(self, other):
        if self.isDir != other.isDir:
            return -1 if self.isDir else 1
        
        if self.filename != other.filename:
            return -1 if self.filename < other.filename else 1
        
        return 0
    
    def renamed(self, newName):
        newFull = self.fullPath[0:-(1+len(self.filename))] + newName
        
        return FileRef(newFull, newName, self.isDir)