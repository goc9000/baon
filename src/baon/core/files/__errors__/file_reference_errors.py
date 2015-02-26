# baon/core/files/__errors__/file_reference_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta

from baon.core.errors.BAONError import BAONError


class FileReferenceError(BAONError, metaclass=ABCMeta):
    pass


class CannotExploreDirectoryError(FileReferenceError):
    def __init__(self, inner_error):
        super(CannotExploreDirectoryError, self).__init__(inner_error=inner_error)

    def _get_format_string(self):
        return 'Cannot open directory for exploration'
