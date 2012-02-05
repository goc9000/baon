import os

class FileRef(object):
    fullPath = None
    filename = None
    isDir = None
    
    def __init__(self, fullPath, filename):
        self.fullPath = fullPath
        self.filename = filename
        self.isDir = os.path.isdir(fullPath)

    def __cmp__(self, other):
        if self.isDir != other.isDir:
            return -1 if self.isDir else 1
        
        if self.filename != other.filename:
            return -1 if self.filename < other.filename else 1
        
        return 0
        