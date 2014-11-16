# baon/core/renaming/RenamedFileReference.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.files.FileReference import FileReference


class RenamedFileReference(FileReference):
    old_file_ref = None
    is_override = False
    
    def __init__(self, old_file_ref, new_filename, problems=None, is_override=False):
        path_length = len(old_file_ref.full_path) - len(old_file_ref.filename)
        new_full_path = old_file_ref.full_path[:path_length] + new_filename

        FileReference.__init__(
            self,
            new_full_path,
            new_filename,
            old_file_ref.is_dir,
            old_file_ref.is_link,
            problems,
        )
        
        self.old_file_ref = old_file_ref
        self.is_override = is_override

    def is_changed(self):
        return self.filename != self.old_file_ref.filename

    def test_repr(self):
        result = FileReference.test_repr(self)

        if self.is_override:
            result += 'OVERRIDE',

        return result
