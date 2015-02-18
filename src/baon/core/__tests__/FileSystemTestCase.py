# baon/core/__tests__/FileSystemTestCase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

import os
import tempfile
import stat

from contextlib import contextmanager
from decorator import decorator

from baon.core.utils.lang_utils import swallow_os_errors


class FileSystemTestCase(TestCase):
    _test_dir_path = ''

    links_supported = None
    unicode_supported = None

    def setUp(self):
        self._test_dir_path = tempfile.mkdtemp()

        self.links_supported = self._check_links_supported()
        self.unicode_supported = os.path.supports_unicode_filenames

    def tearDown(self):
        self.cleanup_files(delete_root=True)

    def _check_links_supported(self):
        full_link_path = self.full_test_path('temp_link')
        full_target_path = self.full_test_path('')

        try:
            os.symlink(full_target_path, full_link_path)
        except OSError:
            return False

        os.unlink(full_link_path)

        return True

    def full_test_path(self, relative_path):
        return os.path.join(self._test_dir_path, relative_path)

    def make_file(self, file_path, read=None, write=None, execute=None):
        dir_name, _ = os.path.split(file_path)
        self.make_dir(dir_name)

        full_file_path = self.full_test_path(file_path)
        with open(full_file_path, 'w') as _:
            pass

        if read is not None or write is not None or execute is not None:
            self.set_rights(file_path, read=read, write=write, execute=execute)

    def make_dir(self, dir_path, read=None, write=None, execute=None):
        full_dir_path = self.full_test_path(dir_path)

        if not os.path.isdir(full_dir_path):
            os.makedirs(full_dir_path)

        if read is not None or write is not None or execute is not None:
            self.set_rights(dir_path, read=read, write=write, execute=execute)

    def make_link(self, link_path, target_path, read=None, write=None, execute=None):
        dir_name, _ = os.path.split(link_path)
        self.make_dir(dir_name)

        full_link_path = self.full_test_path(link_path)
        full_target_path = self.full_test_path(target_path)
        os.symlink(full_target_path, full_link_path)

        if read is not None or write is not None or execute is not None:
            self.set_rights(link_path, read=read, write=write, execute=execute)

    def set_rights(self, path, read=None, write=None, execute=None):
        def adjust_bits(mode, bitmask, condition):
            if condition is True:
                return mode | bitmask
            elif condition is False:
                return mode & ~bitmask
            else:
                return mode

        full_path = self.full_test_path(path)

        current_mode = os.lstat(full_path).st_mode

        current_mode = adjust_bits(current_mode, stat.S_IRUSR, read)
        current_mode = adjust_bits(current_mode, stat.S_IWUSR, write)
        current_mode = adjust_bits(current_mode, stat.S_IXUSR, execute)

        os.lchmod(full_path, current_mode)

    def make_file_structure(self, base_dir, files_repr):
        deferred_set_rights = {}

        for file_repr in files_repr:
            kind, path1, path2, params = _parse_file_repr(file_repr)

            full_path1 = os.path.join(base_dir, path1)
            full_path2 = os.path.join(base_dir, path2) if path2 is not None else None

            other_params = {k: v for k, v in params.items() if k not in {'read', 'write', 'execute'}}

            if kind == 'FILE':
                self.make_file(full_path1, **other_params)
            elif kind == 'DIR':
                self.make_dir(full_path1, **other_params)
            elif kind == 'LINK':
                self.make_link(full_path1, full_path2, **other_params)

            rights = {k: v for k, v in params.items() if k in {'read', 'write', 'execute'}}
            if len(rights) > 0:
                deferred_set_rights[path1] = rights

        for path in reversed(sorted(deferred_set_rights.keys())):
            self.set_rights(os.path.join(base_dir, path), **deferred_set_rights[path])

    def cleanup_files(self, path='', delete_root=False):
        self.set_rights(path, read=True, write=True, execute=True)

        full_path = self.full_test_path(path)

        if os.path.isdir(full_path):
            for item in os.listdir(full_path):
                self.cleanup_files(os.path.join(path, item), True)

        if delete_root:
            if os.path.isdir(full_path):
                os.rmdir(full_path)
            else:
                os.unlink(full_path)

    @contextmanager
    def temp_file_structure(self, base_path, files_repr):
        self.make_file_structure(base_path, files_repr)

        try:
            yield
        finally:
            with swallow_os_errors():
                self.cleanup_files(base_path, base_path != '')

    def assert_is_dir(self, path):
        if not os.path.exists(path):
            self.fail('Path does not exist: {0}'.format(path))
        if not os.path.isdir(path):
            self.fail('Path is not a directory: {0}'.format(path))

    def assert_is_file(self, path):
        if not os.path.exists(path):
            self.fail('Path does not exist: {0}'.format(path))
        if not os.path.isfile(path):
            self.fail('Path is not a file: {0}'.format(path))

    def assert_path_does_not_exist(self, path):
        if os.path.exists(path):
            self.fail('Path should not exist: {0}'.format(path))


@decorator
def requires_links_support(test_method, cls_or_self=None):
    assert cls_or_self is not None, 'This decorator can only be used on a class or instance method'

    if not cls_or_self.links_supported:
        cls_or_self.skipTest('Skipping {0}: Links are not supported on this platform'.format(test_method.__name__))
    else:
        test_method(cls_or_self)


@decorator
def requires_unicode_support(test_method, cls_or_self=None):
    assert cls_or_self is not None, 'This decorator can only be used on a class or instance method'

    if not cls_or_self.links_supported:
        cls_or_self.skipTest(
            'Skipping {0}: Unicode filenames are not supported on this platform'.format(test_method.__name__))
    else:
        test_method(cls_or_self)


def _parse_file_repr(file_repr):
    try:
        kind = file_repr[0]

        if kind in {'FILE', 'DIR'}:
            arity = 1
        elif kind in {'LINK'}:
            arity = 2
        else:
            raise ValueError()

        path1 = file_repr[1]
        path2 = file_repr[2] if arity > 1 else None

        params = dict()
        if len(file_repr) > 1 + arity:
            params = file_repr[1 + arity]

        return kind, path1, path2, params
    except Exception:
        raise AssertionError('Malformed test file representation: {0}'.format(file_repr)) from None
