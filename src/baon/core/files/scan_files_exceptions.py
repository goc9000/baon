# baon/core/files/scan_files_exceptions.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONExceptionBase import BAONExceptionBase


class ScanFilesException(BAONExceptionBase):
    def __init__(self, format_string, error_parameters=None):
        BAONExceptionBase.__init__(self, format_string, error_parameters)


class BasePathDoesNotExistException(ScanFilesException):
    def __init__(self, path):
        ScanFilesException.__init__(
            self, u"Directory '{path}' does not exist",
            {'path': path})


class BasePathIsNotADirectoryException(ScanFilesException):
    def __init__(self, path):
        ScanFilesException.__init__(
            self, u"'{path}' is not a directory",
            {'path': path})


class CannotExploreBasePathException(ScanFilesException):
    def __init__(self, path, inner_exception=None):
        ScanFilesException.__init__(
            self, u"Cannot open directory '{path}' for exploration",
            {'path': path, 'inner_exception': inner_exception})
