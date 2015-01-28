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


class FileSystemTestCase(TestCase):
    _test_dir_path = None

    links_supported = None
    unicode_supported = None

    @classmethod
    def setUpClass(cls):
        cls._test_dir_path = tempfile.mkdtemp()

        cls.links_supported = cls._check_links_supported()
        cls.unicode_supported = os.path.supports_unicode_filenames

    @classmethod
    def tearDownClass(cls):
        cls._cleanup_files(delete_root=True)

    @classmethod
    def _check_links_supported(cls):
        full_link_path = os.path.join(cls._test_dir_path, 'temp_link')
        full_target_path = os.path.join(cls._test_dir_path, '')

        try:
            os.symlink(full_target_path, full_link_path)
        except OSError:
            return False

        os.unlink(full_link_path)

        return True

    @classmethod
    def _make_file(cls, file_path):
        dir_name, _ = os.path.split(file_path)
        cls._make_dir(dir_name)

        full_file_path = os.path.join(cls._test_dir_path, file_path)
        with open(full_file_path, 'w') as _:
            pass

    @classmethod
    def _make_dir(cls, dir_path):
        full_dir_path = os.path.join(cls._test_dir_path, dir_path)

        if not os.path.isdir(full_dir_path):
            os.makedirs(full_dir_path)

    @classmethod
    def _set_rights(cls, path, read=None, write=None, execute=None):
        def adjust_bits(mode, bitmask, condition):
            if condition is True:
                return mode | bitmask
            elif condition is False:
                return mode & ~bitmask
            else:
                return mode

        full_path = os.path.join(cls._test_dir_path, path)

        current_mode = os.lstat(full_path).st_mode

        current_mode = adjust_bits(current_mode, stat.S_IRUSR, read)
        current_mode = adjust_bits(current_mode, stat.S_IWUSR, write)
        current_mode = adjust_bits(current_mode, stat.S_IXUSR, execute)

        os.lchmod(full_path, current_mode)

    @classmethod
    def _make_link(cls, link_path, target_path):
        dir_name, _ = os.path.split(link_path)
        cls._make_dir(dir_name)

        full_link_path = os.path.join(cls._test_dir_path, link_path)
        full_target_path = os.path.join(cls._test_dir_path, target_path)
        os.symlink(full_target_path, full_link_path)

    @classmethod
    def _realize_file_structure(cls, base_dir, files_repr):
        deferred_set_rights = {}

        for file_repr in files_repr:
            kind, path1, path2, params = _parse_file_repr(file_repr)

            if kind == 'FILE':
                cls._make_file(os.path.join(base_dir, path1))
            elif kind == 'DIR':
                cls._make_dir(os.path.join(base_dir, path1))
            elif kind == 'LINK':
                cls._make_link(os.path.join(base_dir, path1), os.path.join(base_dir, path2))

            rights = {k: v for k, v in params.items() if k in {'read', 'write', 'execute'}}
            if len(rights) > 0:
                deferred_set_rights[path1] = rights

        for path in reversed(sorted(deferred_set_rights.keys())):
            cls._set_rights(os.path.join(base_dir, path), **deferred_set_rights[path])

    @classmethod
    def _cleanup_files(cls, path='', delete_root=False):
        cls._set_rights(path, read=True, write=True, execute=True)

        full_path = os.path.join(cls._test_dir_path, path)

        if os.path.isdir(full_path):
            for item in os.listdir(full_path):
                cls._cleanup_files(os.path.join(path, item), True)

        if delete_root:
            if os.path.isdir(full_path):
                os.rmdir(full_path)
            else:
                os.unlink(full_path)

    @classmethod
    @contextmanager
    def _temp_file_structure(cls, base_path, files_repr):
        cls._realize_file_structure(base_path, files_repr)

        exc = None
        try:
            yield
        except Exception as e:
            exc = e

        try:
            cls._cleanup_files(base_path, base_path != '')
        except OSError:
            pass

        if exc is not None:
            raise exc


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
    kind = file_repr[0]

    if kind in {'FILE', 'DIR'}:
        arity = 1
    elif kind in {'LINK'}:
        arity = 2
    else:
        raise RuntimeError('Malformed file representation: {0}'.format(file_repr))

    path1 = file_repr[1]
    path2 = file_repr[2] if arity > 1 else None

    params = dict()
    if len(file_repr) > 1 + arity:
        params = file_repr[1 + arity]

    return kind, path1, path2, params
