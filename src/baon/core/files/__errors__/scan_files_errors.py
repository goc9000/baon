# baon/core/files/__errors__/scan_files_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONError import BAONError


class ScanFilesError(BAONError):
    def __init__(self, format_string, error_parameters=None):
        BAONError.__init__(self, format_string, error_parameters)


class BasePathDoesNotExistError(ScanFilesError):
    def __init__(self, path):
        ScanFilesError.__init__(
            self, "Directory '{path}' does not exist",
            {'path': path})


class BasePathIsNotADirectoryError(ScanFilesError):
    def __init__(self, path):
        ScanFilesError.__init__(
            self, "'{path}' is not a directory",
            {'path': path})


class CannotExploreBasePathError(ScanFilesError):
    def __init__(self, path, inner_error=None):
        ScanFilesError.__init__(
            self, "Cannot open directory '{path}' for exploration",
            {'path': path, 'inner_error': inner_error})
