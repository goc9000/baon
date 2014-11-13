# baon/core/files/FileReference.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


class FileReference(object):
    full_path = None
    filename = None
    is_dir = None
    is_link = None
    
    def __init__(self, full_path, filename, is_dir, is_link):
        self.full_path = full_path
        self.filename = filename
        self.is_dir = is_dir
        self.is_link = is_link

    def __cmp__(self, other):
        if self.is_dir != other.is_dir:
            return -1 if self.is_dir else 1

        return cmp(self.filename, other.filename)

    def _test_repr(self):
        type_str = 'DIR' if self.is_dir else 'FILE'
        if self.is_link:
            type_str = 'LINK:' + type_str

        return type_str, self.filename
