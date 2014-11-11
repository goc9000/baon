# baon/core/files/__tests__/test_FileScanner.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.__tests__.FileSystemTestCase import FileSystemTestCase
from baon.core.files.FileScanner import FileScanner

import os


class TestFileScanner(FileSystemTestCase):
    # TODO: Scan for files that: -cannot be renamed (no write access) - cannot be opened (dirs) - dangling symlinks
    # TODO: Scan for non-existent directory
    # TODO: Test that it reports progress

    @classmethod
    def setup_test_files(cls):
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

        if cls._unicode_supported:
            cls._make_file(u'unicode/\u0111\u0131\u0157/\u0192\u00ef\u0142\u00e9\u2461.txt')
            cls._make_file(u'unicode/\u0192\u00ef\u0142\u00e9\u2460.txt')

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

    def test_unicode_non_recursive(self):
        self._test_file_scanner(
            base_path=u'unicode',
            recursive=False,
            expected_result=(
                ('DIR', u'\u0111\u0131r\u0327'),
                ('FILE', u'\u0192i\u0308\u0142e\u0301\u2460.txt'),
            )
        )

    def test_unicode_recursive(self):
        self._test_file_scanner(
            base_path=u'unicode',
            recursive=True,
            expected_result=(
                ('FILE', u'\u0111\u0131r\u0327/\u0192i\u0308\u0142e\u0301\u2461.txt'),
                ('FILE', u'\u0192i\u0308\u0142e\u0301\u2460.txt'),
            )
        )

    def _test_file_scanner(self, base_path=u'', expected_result=None, **options):
        scanner = FileScanner(**options)
        files = tuple(item._test_repr() for item in scanner.scan(os.path.join(self._test_dir_path, base_path)))

        self.assertEqual(files, expected_result)
