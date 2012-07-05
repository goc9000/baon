import os

class FileRef(object):
    full_path = None
    filename = None
    is_dir = None
    
    def __init__(self, full_path, filename, is_dir = None):
        self.full_path = full_path
        self.filename = filename
        if is_dir is None:
            is_dir = os.path.isdir(full_path)
        self.is_dir = is_dir

    def __cmp__(self, other):
        if self.is_dir != other.is_dir:
            return -1 if self.is_dir else 1
        
        if self.filename != other.filename:
            return -1 if self.filename < other.filename else 1
        
        return 0
    
    def renamed(self, new_name):
        if new_name is not None:
            new_full = self.full_path[0:(len(self.full_path)-len(self.filename))] + new_name
        else:
            new_full = None
        
        return RenamedFileRef(new_full, new_name, self.is_dir, self.full_path, self.filename)

from RenamedFileRef import RenamedFileRef