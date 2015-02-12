# baon/core/files/__errors__/file_reference_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONError import BAONError


class FileReferenceError(BAONError):
    def __init__(self, format_string, error_parameters=None):
        BAONError.__init__(self, format_string, error_parameters)


class CannotExploreDirectoryError(FileReferenceError):
    def __init__(self, inner_error=None):
        FileReferenceError.__init__(
            self, 'Cannot open directory for exploration',
            {'inner_error': inner_error})
