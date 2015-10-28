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

    def __eq__(self, other):
        self.assert_compatible_with(other)
        return self.components == other.components

    def __hash__(self):
        return self.path_text().__hash__()

    def is_root(self):
        return len(self.components) == 0

    def is_virtual(self):
        return self.base_path is None

    def is_sane(self):
        return not any(
            (re.match('^(|[.]+)$', c)) or (os.path.sep in c)
            for c in self.components
        )

    def basename(self):
        assert not self.is_root(), 'Basename is not defined for root path'
        return self.components[-1]

    def parent_paths(self):
        for i in range(1, len(self.components)):
            yield BAONPath(self.base_path, self.components[:i])

    def real_path(self):
        assert not self.is_virtual(), 'Cannot materialize virtual path'
        assert self.is_sane(), 'Path fails sanity check before materialization' + repr(self.components)

        return os.path.join(self.base_path, *self.components)

    def path_text(self):
        return os.path.sep.join(self.components)

    def test_repr(self):
        return '/'.join(self.components)

    def assert_compatible_with(self, other):
        assert self.base_path == other.base_path, 'Paths defined on different base paths are incompatible'

    def extend(self, component):
        return BAONPath(self.base_path, self.components + [component])

    def replace_path_text(self, new_path_text):
        return BAONPath.from_path_text(self.base_path, new_path_text)

    def replace_basename(self, new_basename):
        assert not self.is_root(), 'Basename is not defined for root path'
        return BAONPath(self.base_path, self.components[:-1] + [new_basename])

    @staticmethod
    def from_path_text(base_path, path_text):
        return BAONPath(base_path, path_text.split(os.path.sep))

    @staticmethod
    def from_test_repr(base_path, path_repr):
        return BAONPath(base_path, path_repr.split('/'))
