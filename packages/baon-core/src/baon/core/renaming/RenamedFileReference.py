# baon/core/renaming/RenamedFileReference.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONError import BAONError
from baon.core.files.BAONPath import BAONPath
from baon.core.files.FileReference import FileReference
from baon.core.utils.lang_utils import is_arrayish


class RenamedFileReference(FileReference):
    old_file_ref = None
    is_override = False
    
    def __init__(self, old_file_ref, new_path, problems=None, is_override=False):
        old_file_ref.path.assert_compatible_with(new_path)

        super().__init__(
            new_path,
            old_file_ref.is_dir,
            old_file_ref.is_link,
            problems,
        )
        
        self.old_file_ref = old_file_ref
        self.is_override = is_override

    def is_changed(self):
        return self.path != self.old_file_ref.path

    def test_repr(self):
        result = super().test_repr()

        if self.is_override:
            result += 'OVERRIDE',

        return result

    @staticmethod
    def from_test_repr(file_test_repr, base_path=None):
        assert is_arrayish(file_test_repr)
        assert len(file_test_repr) >= 2

        file_type, old_path, *remainder = file_test_repr

        old_file_ref = FileReference(
            BAONPath.from_test_repr(base_path, old_path),
            file_type == 'DIR',
        )

        new_path = old_path
        override = False

        if len(remainder) > 0 and remainder[-1] == 'OVERRIDE':
            remainder = remainder[:-1]
            override = True

        if len(remainder) > 0 and not is_arrayish(remainder[0]):
            new_path, *remainder = remainder

        return RenamedFileReference(
            old_file_ref,
            BAONPath.from_test_repr(base_path, new_path),
            [BAONError.from_test_repr(error_repr) for error_repr in remainder],
            override,
        )
