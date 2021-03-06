# baon/core/files/BAONPath.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os
import re

from functools import total_ordering


@total_ordering
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

    def __lt__(self, other):
        self.assert_compatible_with(other)
        return self.components < other.components

    def __hash__(self):
        return self.path_text().__hash__()

    def equals_ignore_case(self, other):
        self.assert_compatible_with(other)
        return (
            (len(self.components) == len(other.components)) and
            all(a.lower() == b.lower() for a, b in zip(self.components, other.components))
        )

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

    def parent_path(self):
        assert not self.is_root(), 'Parent paths are not defined for root path'
        return BAONPath(self.base_path, self.components[:-1])

    def parent_paths(self):
        assert not self.is_root(), 'Parent paths are not defined for root path'

        for path in self.subpaths(exclude_self=True):
            yield path

    def subpaths(self, exclude_self=False, exclude_root=False):
        range_start = 1 if exclude_root else 0
        range_end = len(self.components) + (0 if exclude_self else 1)

        for i in range(range_start, range_end):
            yield BAONPath(self.base_path, self.components[:i])

    def real_path(self):
        assert not self.is_virtual(), 'Cannot materialize virtual path'
        assert self.is_sane(), 'Path fails sanity check before materialization: ' + repr(self.components)

        return os.path.join(self.base_path, *self.components)

    def path_text(self):
        return os.path.sep.join(self.components)

    def test_repr(self):
        return '/'.join(self.components)

    def assert_compatible_with(self, other):
        assert self.base_path == other.base_path, 'Paths defined on different base paths are incompatible'

    def extend(self, component):
        assert os.path.sep not in component, 'Attempt to extend with path text instead of single component'

        return BAONPath(self.base_path, self.components + [component])

    def extend_with_path_text(self, path_text):
        return BAONPath(self.base_path, self.components + path_text.split(os.path.sep))

    def replace_path_text(self, new_path_text):
        return BAONPath.from_path_text(self.base_path, new_path_text)

    def replace_basename(self, new_basename):
        assert not self.is_root(), 'Basename is not defined for root path'
        assert os.path.sep not in new_basename, 'Attempt to replace basename with path text instead of single component'

        return BAONPath(self.base_path, self.components[:-1] + [new_basename])

    @staticmethod
    def from_path_text(base_path, path_text):
        return BAONPath(base_path, path_text.split(os.path.sep))

    @staticmethod
    def from_test_repr(base_path, path_repr):
        return BAONPath(base_path, path_repr.split('/'))

    @staticmethod
    def assert_all_compatible(*paths):
        for path in paths:
            paths[0].assert_compatible_with(path)
