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
    _links_supported = None

    # TODO: Scan for files that: -cannot be renamed (no write access) - cannot be opened (dirs) - dangling symlinks
    # TODO: Scan for non-existent directory
    # TODO: Scan for unicode files (check out os.path.supports_unicode_filenames)
    # TODO: Do not follow symlinks
    # TODO: Test that it reports progress

    @classmethod
    def setUpClass(cls):
        cls._test_dir_path = tempfile.mkdtemp()
        cls._links_supported = cls._check_links_supported()

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

        if cls._links_supported:
            cls._make_link('links/link1', 'basic/file2.bin')
            cls._make_link('links/link2', 'basic/dir1')
            cls._make_link('links/link3', 'dangling')

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

    def test_links_non_recursive(self):
        if not self._links_supported:
            self.skipTest('Skipping test_links_non_recursive: Symlinks are not supported on this platform')

        self._test_file_scanner(
            base_path=u'links',
            recursive=False,
            expected_result=(
                ('LINK:DIR', u'link2'),
                ('LINK:FILE', u'link1'),
                ('LINK:FILE', u'link3'),
            )
        )

    def test_links_recursive(self):
        if not self._links_supported:
            self.skipTest('Skipping test_links_recursive: Symlinks are not supported on this platform')

        self._test_file_scanner(
            base_path=u'links',
            recursive=True,
            expected_result=(
                ('LINK:DIR', u'link2'),  # Symlinks are not followed even in recursive mode
                ('LINK:FILE', u'link1'),
                ('LINK:FILE', u'link3'),
            )
        )

    def _test_file_scanner(self, base_path=u'', expected_result=None, **options):
        scanner = FileScanner(**options)
        files = tuple(item._test_repr() for item in scanner.scan(os.path.join(self._test_dir_path, base_path)))

        self.assertEqual(files, expected_result)
