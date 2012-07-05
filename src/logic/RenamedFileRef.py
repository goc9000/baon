from FileRef import FileRef

class RenamedFileRef(FileRef):
    old_full_path = None
    old_filename = None
    error = None
    warning = None
    name_override = None
    
    def __init__(self, full_path, filename, is_dir, old_full_path, old_filename):
        FileRef.__init__(self, full_path, filename, is_dir)
        
        self.old_full_path = old_full_path
        self.old_filename = old_filename
