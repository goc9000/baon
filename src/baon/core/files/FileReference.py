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
    
    def __init__(self, full_path, filename, is_dir):
        self.full_path = full_path
        self.filename = filename
        self.is_dir = is_dir

    def __cmp__(self, other):
        if self.is_dir != other.is_dir:
            return -1 if self.is_dir else 1
        
        if self.filename != other.filename:
            return -1 if self.filename < other.filename else 1
        
        return 0
