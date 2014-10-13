# baon/core/files/__tests__/test_FileScanner.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.core.files.FileScanner import FileScanner


import os
import tempfile
import shutil


class TestFileScanner(TestCase):
    _test_dir_path = None

    # TODO: Scan for files that: -cannot be renamed (no write access) - cannot be opened (dirs)
    # TODO: Scan for unicode files
    # TODO: Do not follow symlinks

    @classmethod
    def setUpClass(cls):
        cls._test_dir_path = tempfile.mkdtemp()

        cls._make_file('basic/dir1/file11.txt')
        cls._make_file('basic/dir1/file12')
        cls._make_file('basic/dir2/dir21/file211')
        cls._make_file('basic/dir2/dir21/file212')
        cls._make_file('basic/dir2/dir22/file221.bin')
        cls._make_file('basic/dir2/file21')
        cls._make_dir('basic/dir3/dir31')
        cls._make_file('basic/dir3/dir32/file321.txt')
        cls._make_file('basic/file1')
        cls._make_file('basic/file2.bin')
        cls._make_file('basic/file3')

        cls._make_dir('empties/empty')
        cls._make_dir('empties/dir1/empty1')
        cls._make_file('empties/dir1/file1')

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
    def tearDownClass(cls):
        shutil.rmtree(cls._test_dir_path)

    def test_basic_non_recursive(self):
        self._test_file_scanner(
            base_path=u'basic',
            recursive=False,
            expected_result=(
                ('DIR', u'dir1'),
                ('DIR', u'dir2'),
                ('DIR', u'dir3'),
                ('FILE', u'file1'),
                ('FILE', u'file2.bin'),
                ('FILE', u'file3'),
            )
        )

    def test_basic_recursive(self):
        self._test_file_scanner(
            base_path=u'basic',
            recursive=True,
            expected_result=(
                ('FILE', u'dir1/file11.txt'),
                ('FILE', u'dir1/file12'),
                ('FILE', u'dir2/dir21/file211'),
                ('FILE', u'dir2/dir21/file212'),
                ('FILE', u'dir2/dir22/file221.bin'),
                ('FILE', u'dir2/file21'),
                ('FILE', u'dir3/dir32/file321.txt'),
                ('FILE', u'file1'),
                ('FILE', u'file2.bin'),
                ('FILE', u'file3'),
            )
        )

    def test_empty_dirs_non_recursive(self):
        self._test_file_scanner(
            base_path=u'empties',
            recursive=False,
            expected_result=(
                ('DIR', u'dir1'),
                ('DIR', u'empty'),
            )
        )

    def test_empty_dirs_recursive(self):
        self._test_file_scanner(
            base_path=u'empties',
            recursive=True,
            expected_result=(
                ('FILE', u'dir1/file1'),
            )
        )

    def _test_file_scanner(self, base_path=u'', expected_result=None, **options):
        scanner = FileScanner(**options)
        files = tuple(item._test_repr() for item in scanner.scan(os.path.join(self._test_dir_path, base_path)))

        self.assertEqual(files, expected_result)
