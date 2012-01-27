import os

from FileRef import FileRef

class FileScanner(object):
    def __init__(self):
        pass
    
    def scan(self, basePath):
        if not os.path.exists(basePath):
            raise RuntimeError("Path '{0}' does not exist".format(basePath))
        if not os.path.isdir(basePath):
            raise RuntimeError("'{0}' is not a directory".format(basePath))
        
        rawFiles = os.listdir(basePath)
        files = sorted([ FileRef(os.path.join(basePath, name), name) for name in rawFiles ])
        
        return files
        