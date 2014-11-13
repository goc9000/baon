# baon/core/files/file_reference_exceptions.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONExceptionBase import BAONExceptionBase


class FileReferenceException(BAONExceptionBase):
    def __init__(self, format_string, error_parameters=None):
        BAONExceptionBase.__init__(self, format_string, error_parameters)


class CannotExploreDirectoryException(FileReferenceException):
    def __init__(self, inner_exception=None):
        FileReferenceException.__init__(
            self, u"Cannot open directory for exploration",
            {'inner_exception': inner_exception})
