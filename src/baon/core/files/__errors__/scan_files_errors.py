# baon/core/files/__errors__/scan_files_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta

from baon.core.errors.BAONError import BAONError


class ScanFilesError(BAONError, metaclass=ABCMeta):
    pass


class BasePathDoesNotExistError(ScanFilesError):
    def __init__(self, path):
        super(BasePathDoesNotExistError, self).__init__(path=path)

    def _get_format_string(self):
        return "Directory '{path}' does not exist"


class BasePathIsNotADirectoryError(ScanFilesError):
    def __init__(self, path):
        super(BasePathIsNotADirectoryError, self).__init__(path=path)

    def _get_format_string(self):
        return "'{path}' is not a directory"


class CannotExploreBasePathError(ScanFilesError):
    def __init__(self, path, inner_error):
        super(CannotExploreBasePathError, self).__init__(path=path, inner_error=inner_error)

    def _get_format_string(self):
        return "Cannot open directory '{path}' for exploration"
