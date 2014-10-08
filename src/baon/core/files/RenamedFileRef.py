# baon/core/files/RenamedFileRef.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.files.FileRef import FileRef


class RenamedFileRef(FileRef):
    old_full_path = None
    old_filename = None
    error = None
    warning = None
    override = False
    
    def __init__(self, old_file_ref, new_filename, override=False):
        if new_filename is not None:
            path_length = len(old_file_ref.full_path) - len(old_file_ref.filename)
            new_full_path = old_file_ref.full_path[:path_length] + new_filename
        else:
            new_full_path = None
        
        FileRef.__init__(self, new_full_path, new_filename, old_file_ref.is_dir)
        
        self.old_full_path = old_file_ref.full_path
        self.old_filename = old_file_ref.filename
        self.override = override

    def changed(self):
        return self.filename != self.old_filename
