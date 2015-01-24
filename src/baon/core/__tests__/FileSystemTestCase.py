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
import shutil
import stat
import inspect


class FileSystemTestCase(TestCase):
    _test_dir_path = None
    _links_supported = None
    _unicode_supported = None

    _restore_rights_stack = None

    @classmethod
    def setUpClass(cls):
        cls._test_dir_path = tempfile.mkdtemp()
        cls._links_supported = cls._check_links_supported()
        cls._unicode_supported = os.path.supports_unicode_filenames
        cls._restore_rights_stack = list()

        cls.setup_test_files()
        for name, method in inspect.getmembers(cls, inspect.ismethod):
            if name.startswith('setup_test_files_'):
                method()

    @classmethod
    def setup_test_files(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        for path, mode in reversed(cls._restore_rights_stack):
            os.chmod(path, mode)

        shutil.rmtree(cls._test_dir_path)

    @classmethod
    def _make_file(cls, file_path):
        dir_name, _ = os.path.split(file_path)
        cls._make_dir(dir_name)

        full_file_path = os.path.join(cls._test_dir_path, file_path)
        with file(full_file_path, 'w') as _:
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
        cls._restore_rights_stack.append((full_path, current_mode))

        current_mode = adjust_bits(current_mode, stat.S_IRUSR, read)
        current_mode = adjust_bits(current_mode, stat.S_IWUSR, write)
        current_mode = adjust_bits(current_mode, stat.S_IXUSR, execute)

        os.lchmod(full_path, current_mode)

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

            rights = {k: v for k, v in params.iteritems() if k in {'read', 'write', 'execute'}}
            if len(rights) > 0:
                deferred_set_rights[path1] = rights

        for path in reversed(sorted(deferred_set_rights.keys())):
            cls._set_rights(os.path.join(base_dir, path), **deferred_set_rights[path])


def _parse_file_repr(file_repr):
    kind = file_repr[0]

    if kind in {'FILE', 'DIR'}:
        arity = 1
    elif kind in {'LINK'}:
        arity = 2
    else:
        raise RuntimeError(u'Malformed file representation: {0}'.format(file_repr))

    path1 = file_repr[1]
    path2 = file_repr[2] if arity > 1 else None

    params = dict()
    if len(file_repr) > 1 + arity:
        params = file_repr[1 + arity]

    return kind, path1, path2, params
