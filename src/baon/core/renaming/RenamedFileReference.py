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
    
    def __init__(self, old_file_ref, new_path, problems=None, is_override=False):
        super().__init__(
            new_path,
            old_file_ref.is_dir,
            old_file_ref.is_link,
            problems,
        )
        
        self.old_file_ref = old_file_ref
        self.is_override = is_override

    def is_changed(self):
        return self.filename != self.old_file_ref.filename

    def test_repr(self):
        result = super().test_repr()

        if self.is_override:
            result += 'OVERRIDE',

        return result
