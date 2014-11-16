# baon/core/files/FileReference.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import itertools

from baon.core.files.baon_paths import all_path_components


class FileReference(object):
    full_path = None
    filename = None
    is_dir = None
    is_link = None
    problems = None
    
    def __init__(self, full_path, filename, is_dir, is_link=False, problems=None):
        self.full_path = full_path
        self.filename = filename
        self.is_dir = is_dir
        self.is_link = is_link
        self.problems = list() if problems is None else problems

    def __cmp__(self, other):
        my_components = all_path_components(self.filename)
        other_components = all_path_components(other.filename)

        for i in itertools.count():
            my_head = my_components[i] if i < len(my_components) else None
            other_head = other_components[i] if i < len(other_components) else None

            if my_head is None and other_head is None:
                return 0
            if my_head is None:
                return -1 if my_head is None else 1

            my_head_is_dir = True if i < len(my_components) - 1 else self.is_dir
            other_head_is_dir = True if i < len(other_components) - 1 else other.is_dir

            if my_head_is_dir != other_head_is_dir:
                return -1 if my_head_is_dir else 1
            if my_head != other_head:
                return -1 if my_head < other_head else 1

    def test_repr(self):
        type_str = 'DIR' if self.is_dir else 'FILE'
        if self.is_link:
            type_str = 'LINK:' + type_str

        repr_tuple = type_str, self.filename

        if len(self.problems) > 0:
            repr_tuple += tuple(problem.__class__.__name__ for problem in self.problems),

        return repr_tuple
