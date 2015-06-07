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

    def __lt__(self, other):
        return self.compare(self, other) < 0

    def has_problems(self):
        return len(self.problems) > 0

    def has_errors(self):
        return self.error_count() > 0

    def has_warnings(self):
        return self.warning_count() > 0

    def error_count(self):
        return len(self.errors())

    def warning_count(self):
        return len(self.warnings())

    def errors(self):
        return [error for error in self.problems if not isinstance(error, Warning)]

    def warnings(self):
        return [warning for warning in self.problems if isinstance(warning, Warning)]

    def test_repr(self):
        type_str = 'DIR' if self.is_dir else 'FILE'
        if self.is_link:
            type_str = 'LINK:' + type_str

        repr_tuple = type_str, self.filename

        if len(self.problems) > 0:
            repr_tuple += tuple(problem.__class__.__name__ for problem in self.problems),

        return repr_tuple

    @staticmethod
    def compare(ref_a, ref_b):
        a_components = all_path_components(ref_a.filename)
        b_components = all_path_components(ref_b.filename)

        for i in itertools.count():
            a_head = a_components[i] if i < len(a_components) else None
            b_head = b_components[i] if i < len(b_components) else None

            if a_head is None and b_head is None:
                return 0
            if a_head is None or b_head is None:
                return -1 if a_head is None else 1

            a_head_is_dir = True if i < len(a_components) - 1 else ref_a.is_dir
            b_head_is_dir = True if i < len(b_components) - 1 else ref_b.is_dir

            if a_head_is_dir != b_head_is_dir:
                return -1 if a_head_is_dir else 1
            if a_head != b_head:
                return -1 if a_head < b_head else 1
