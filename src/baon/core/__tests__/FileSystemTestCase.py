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

        os.chmod(full_path, current_mode)

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
