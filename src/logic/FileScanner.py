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
        
        return self._scan(base_path, '', recursive)

    def _scan(self, base_path, rel_path, recursive):
        files = []
        
        path = os.path.join(base_path, rel_path)
        
        raw_files = os.listdir(path)
        files_here = sorted([ FileRef(os.path.join(path, name), os.path.join(rel_path, name)) for name in raw_files ])
        
        for f in files_here:
            if f.is_dir and recursive:
                sub_files = self._scan(base_path, f.filename, recursive)
                if len(sub_files) > 0:
                    files.extend(sub_files)
                    continue
            files.append(f)
        
        return files
