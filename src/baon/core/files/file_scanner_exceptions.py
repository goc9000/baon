# baon/core/files/file_scanner_exceptions.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONExceptionBase import BAONExceptionBase


class FileScannerException(BAONExceptionBase):
    def __init__(self, format_string, error_parameters=None):
        BAONExceptionBase.__init__(self, format_string, error_parameters)


class BasePathDoesNotExistException(FileScannerException):
    def __init__(self, path):
        FileScannerException.__init__(
            self, u"Directory '{path}' does not exist",
            {'path': path})


class BasePathIsNotADirectoryException(FileScannerException):
    def __init__(self, path):
        FileScannerException.__init__(
            self, u"'{path}' is not a directory",
            {'path': path})


class CannotExploreBasePathException(FileScannerException):
    def __init__(self, path, inner_exception=None):
        FileScannerException.__init__(
            self, u"Cannot open directory '{path}' for exploration",
            {'path': path, 'inner_exception': inner_exception})


class CannotExploreDirectoryException(FileScannerException):
    def __init__(self, inner_exception=None):
        FileScannerException.__init__(
            self, u"Cannot open directory for exploration",
            {'inner_exception': inner_exception})
