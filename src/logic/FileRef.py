import os

class FileRef(object):
    fullPath = None
    filename = None
    isDir = None
    
    def __init__(self, fullPath, filename):
        self.fullPath = fullPath
        self.filename = filename
        self.isDir = os.path.isdir(fullPath)
