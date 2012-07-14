# logic/FileScanner.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import os

from FileRef import FileRef

class FileScanner(object):
    def __init__(self):
        pass
    
    def scan(self, base_path, recursive, on_progress=None):
        if not os.path.exists(base_path):
            raise RuntimeError("Path '{0}' does not exist".format(base_path))
        if not os.path.isdir(base_path):
            raise RuntimeError("'{0}' is not a directory".format(base_path))
        
        stats = dict(done=0, total=1)
        
        return self._scan(base_path, '', recursive, stats, on_progress)

    def _scan(self, base_path, rel_path, recursive, stats, on_progress):
        files = []
        
        path = os.path.join(base_path, rel_path)
        
        raw_files = os.listdir(path)
        files_here = sorted([ FileRef(os.path.join(path, name), os.path.join(rel_path, name)) for name in raw_files ])
        
        stats['done'] += 1
        stats['total'] += len(files_here)
        if on_progress is not None:
            on_progress(stats['done'], stats['total'])
        
        for f in files_here:
            if f.is_dir and recursive:
                sub_files = self._scan(base_path, f.filename, recursive, stats, on_progress)
                if len(sub_files) > 0:
                    files.extend(sub_files)
                    continue
            files.append(f)
            
            stats['done'] += 1
            if on_progress is not None:
                on_progress(stats['done'], stats['total'])
        
        return files
