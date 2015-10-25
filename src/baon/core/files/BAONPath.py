# baon/core/files/BAONPath.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os
import re


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

    def is_virtual(self):
        return self.base_path is None

    def is_sane(self):
        return not any(
            (re.match('^(|[.]+)$', c)) or (os.path.sep in c)
            for c in self.components
        )

    def real_path(self):
        assert not self.is_virtual(), 'Cannot materialize virtual path'
        assert self.is_sane(), 'Path fails sanity check before materialization' + repr(self.components)

        return os.path.join(self.base_path, *self.components)

    def path_text(self):
        return os.path.sep.join(self.components)

    def extend(self, component):
        return BAONPath(self.base_path, self.components + [component])

    @staticmethod
    def from_path_text(base_path, path_text):
        return BAONPath(base_path, path_text.split(os.path.sep))

    @staticmethod
    def from_test_repr(base_path, path_repr):
        return BAONPath(base_path, path_repr.split('/'))
