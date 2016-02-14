# baon/core/__tests__/FileSystemTestCase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os
import platform
import tempfile
from contextlib import contextmanager
from unittest import TestCase

from decorator import decorator

from baon.core.utils.file_utils import check_filesystem_at_path_case_insensitive, set_file_rights
from baon.core.utils.lang_utils import swallow_os_errors


class FileSystemTestCase(TestCase):
    """
    Note: the file functions here work with respect to a temporary test directory. Any files created there are
    automatically deleted at the end of the test. In order to write or read files externally, you have to specify
    absolute paths. Note that external files are not deleted automatically.
    """

    _test_dir_path = ''

    links_supported = None
    unicode_supported = None
    case_insensitive_filesystem = None
    posix_filesystem = None

    def setUp(self):
        super().setUp()

        self._test_dir_path = tempfile.mkdtemp()

        self.links_supported = self._check_links_supported()
        self.unicode_supported = os.path.supports_unicode_filenames
        self.case_insensitive_filesystem = self._check_case_insensitive_filesystem()
        self.posix_filesystem = platform.system() in ['Linux', 'Darwin']

    def tearDown(self):
        self.cleanup_files(delete_root=True)

        super().tearDown()

    def _check_links_supported(self):
        full_link_path = self.resolve_test_path('temp_link')
        full_target_path = self.resolve_test_path('')

        try:
            os.symlink(full_target_path, full_link_path)
        except OSError:
            return False

        os.unlink(full_link_path)

        return True

    def _check_case_insensitive_filesystem(self):
        return check_filesystem_at_path_case_insensitive(self._test_dir_path)

    def resolve_test_path(self, relative_path):
        return os.path.join(self._test_dir_path, relative_path)

    def open_file(self, path, *args):
        return open(self.resolve_test_path(path), *args)

    def make_file(self, path, contents=None, read=None, write=None, execute=None):
        dir_name, _ = os.path.split(path)
        self.make_dir(dir_name)

        with self.open_file(path, 'w') as f:
            if contents is not None:
                f.write(contents)

        self.set_rights(path, read=read, write=write, execute=execute)

    def make_dir(self, path, read=None, write=None, traverse=None):
        full_dir_path = self.resolve_test_path(path)

        if not os.path.isdir(full_dir_path):
            os.makedirs(full_dir_path)

        self.set_rights(path, read=read, write=write, traverse=traverse)

    def make_link(self, link_path, target_path, read=None, write=None, execute=None, traverse=None):
        dir_name, _ = os.path.split(link_path)
        self.make_dir(dir_name)

        full_link_path = self.resolve_test_path(link_path)
        full_target_path = self.resolve_test_path(target_path)
        os.symlink(full_target_path, full_link_path)

        self.set_rights(link_path, read=read, write=write, execute=execute, traverse=traverse)

    def set_rights(self, path, read=None, write=None, execute=None, traverse=None):
        assert traverse != False or self.posix_filesystem, 'Traverse permission only makes sense in POSIX filesystems'

        set_file_rights(self.resolve_test_path(path), read=read, write=write, execute=execute, traverse=traverse)

    def make_file_structure(self, base_dir, files_repr):
        deferred_set_rights = {}

        for file_repr in files_repr:
            kind, path1, path2, permissions = _parse_file_repr(file_repr)

            full_path1 = os.path.join(base_dir, path1)
            full_path2 = os.path.join(base_dir, path2) if path2 is not None else None

            if kind == 'FILE':
                self.make_file(full_path1)
            elif kind == 'DIR':
                self.make_dir(full_path1)
            elif kind == 'LINK':
                self.make_link(full_path1, full_path2)
            else:
                raise AssertionError('Unrecognized file type {0}'.format(kind))

            if len(permissions) > 0:
                deferred_set_rights[path1] = permissions

        for path in reversed(sorted(deferred_set_rights.keys())):
            self.set_rights(os.path.join(base_dir, path), **deferred_set_rights[path])

    def cleanup_files(self, path='', delete_root=False):
        full_path = self.resolve_test_path(path)

        if os.path.isdir(full_path):
            self.set_rights(path, read=True, write=True, traverse=True)
            for item in os.listdir(full_path):
                self.cleanup_files(os.path.join(path, item), True)
        else:
            self.set_rights(path, read=True, write=True)

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
        self.assert_path_exists(path)

        if not os.path.isdir(self.resolve_test_path(path)):
            self.fail('Path is not a directory: {0}'.format(path))

    def assert_is_file(self, path):
        self.assert_path_exists(path)

        if not os.path.isfile(self.resolve_test_path(path)):
            self.fail('Path is not a file: {0}'.format(path))

    def assert_path_exists(self, path):
        if not os.path.exists(self.resolve_test_path(path)):
            self.fail('Path does not exist: {0}'.format(path))

    def assert_path_does_not_exist(self, path):
        if os.path.exists(self.resolve_test_path(path)):
            self.fail('Path should not exist: {0}'.format(path))

    def assert_file_contents(self, path, contents):
        self.assertEqual(self.get_file_contents(path), contents)

    def assert_file_contents_not(self, path, contents):
        self.assertNotEqual(self.get_file_contents(path), contents)

    def get_file_contents(self, path):
        self.assert_is_file(path)

        with self.open_file(path, 'rt') as f:
            return f.read()


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


@decorator
def requires_case_insensitive_filesystem(test_method, cls_or_self=None):
    assert cls_or_self is not None, 'This decorator can only be used on a class or instance method'

    if not cls_or_self.case_insensitive_filesystem:
        cls_or_self.skipTest(
            'Skipping {0}: Test requires case insensitive filesystem'.format(test_method.__name__))
    else:
        test_method(cls_or_self)


@decorator
def requires_posix_filesystem(test_method, cls_or_self=None):
    assert cls_or_self is not None, 'This decorator can only be used on a class or instance method'

    if not cls_or_self.posix_filesystem:
        cls_or_self.skipTest(
            'Skipping {0}: Test requires POSIX filesystem (Linux or Mac)'.format(test_method.__name__))
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

        permissions = dict()

        for item in file_repr[1 + arity:]:
            if item == '#noread':
                permissions['read'] = False
            elif item == '#nowrite':
                permissions['write'] = False
            elif item == '#noexecute':
                permissions['execute'] = False
            elif item == '#notraverse':
                permissions['traverse'] = False
            else:
                raise ValueError()

        return kind, path1, path2, permissions
    except Exception:
        raise AssertionError('Malformed test file representation: {0}'.format(file_repr)) from None
