# baon/core/files/BAONPath.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os


class BAONPath(object):
    """
    Paths for scanned files in BAON have slightly different processing rules to those in os.path, enough to warrant
    a specialized class for manipulating these paths. BAON paths are always relative to a given "real" base path, and
    only paths that belong to the same base path may interact.
    """
    base_path = None
    components = None

    def __init__(self, base_path, components=None):
        self.base_path = base_path
        self.components = components or []

    def is_root(self):
        return len(self.components) == 0

    def real_path(self):
        return os.path.join(self.base_path, *self.components)

    def real_relative_path(self):
        return '.' if self.is_root() else os.path.join(*self.components)

    def extend(self, component):
        return BAONPath(self.base_path, self.components + [component])
