# baon/core/files/__errors__/file_reference_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta

from baon.core.errors.BAONError import BAONError
from baon.core.errors.BAONWarning import BAONWarning


class FileReferenceError(BAONError, metaclass=ABCMeta):
    pass


class CannotExploreDirectoryError(FileReferenceError):
    def __init__(self, inner_error):
        super().__init__(inner_error=inner_error)

    def _get_format_string(self):
        return 'Cannot open directory for exploration'


class SyntheticFileError(FileReferenceError):
    def __init__(self):
        super().__init__()

    def _get_format_string(self):
        return 'Synthetic error (used in tests)'


class FileReferenceWarning(BAONWarning):
    pass


class SyntheticFileWarning(FileReferenceWarning):
    def __init__(self):
        super().__init__()

    def _get_format_string(self):
        return 'Synthetic warning (used in tests)'
