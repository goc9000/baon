import os

from FileRef import FileRef

class FileScanner(object):
    def __init__(self):
        pass
    
    def scan(self, base_path, recursive):
        if not os.path.exists(base_path):
            raise RuntimeError("Path '{0}' does not exist".format(base_path))
        if not os.path.isdir(base_path):
            raise RuntimeError("'{0}' is not a directory".format(base_path))
        
        if recursive:
            raise RuntimeError("Recursive scan NIY")
        
        raw_files = os.listdir(base_path)
        files = sorted([ FileRef(os.path.join(base_path, name), name) for name in raw_files ])
        
        return files
        