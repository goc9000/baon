# baon/core/files/__tests__/test_scan_files.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.__tests__.FileSystemTestCase import FileSystemTestCase
from baon.core.__tests__.ReportsProgressTestCase import ReportsProgressTestCase

from baon.core.files.scan_files import scan_files
from baon.core.files.scan_files_exceptions import BasePathDoesNotExistException, BasePathIsNotADirectoryException,\
    CannotExploreBasePathException


class TestScanFiles(FileSystemTestCase, ReportsProgressTestCase):

    @classmethod
    def setup_test_files_basic(cls):
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

    @classmethod
    def setup_test_files_empties(cls):
        cls._make_dir('empties/empty')
        cls._make_dir('empties/dir1/empty1')
        cls._make_file('empties/dir1/file1')

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

    @classmethod
    def setup_test_files_links(cls):
        if cls._links_supported:
            cls._make_link('links/link1', 'basic/file2.bin')
            cls._make_link('links/link2', 'basic/dir1')
            cls._make_link('links/link3', 'dangling')

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

    @classmethod
    def setup_test_files_unicode(cls):
        if cls._unicode_supported:
            cls._make_file(u'unicode/\u0111\u0131\u0157/\u0192\u00ef\u0142\u00e9\u2461.txt')
            cls._make_file(u'unicode/\u0192\u00ef\u0142\u00e9\u2460.txt')

    def test_unicode_non_recursive(self):
        if not self._unicode_supported:
            self.skipTest('Skipping test_unicode_non_recursive: Unicode filenames are not supported on this platform')

        self._test_file_scanner(
            base_path=u'unicode',
            recursive=False,
            expected_result=(
                ('DIR', u'\u0111\u0131r\u0327'),
                ('FILE', u'\u0192i\u0308\u0142e\u0301\u2460.txt'),
            )
        )

    def test_unicode_recursive(self):
        if not self._unicode_supported:
            self.skipTest('Skipping test_unicode_recursive: Unicode filenames are not supported on this platform')

        self._test_file_scanner(
            base_path=u'unicode',
            recursive=True,
            expected_result=(
                ('FILE', u'\u0111\u0131r\u0327/\u0192i\u0308\u0142e\u0301\u2461.txt'),
                ('FILE', u'\u0192i\u0308\u0142e\u0301\u2460.txt'),
            )
        )

    @classmethod
    def setup_test_files_permissions(cls):
        cls._make_file('permissions/normal_dir/file11.txt')
        cls._make_file('permissions/normal_dir/file12.txt')
        cls._make_file('permissions/no_read_dir/file21.txt')
        cls._make_file('permissions/no_read_dir/file22.txt')
        cls._set_rights('permissions/no_read_dir', read=False)
        cls._make_file('permissions/no_exec_dir/file31.txt')
        cls._make_file('permissions/no_exec_dir/file32.txt')
        cls._set_rights('permissions/no_exec_dir', execute=False)
        cls._make_file('permissions/normal.txt')
        cls._make_file('permissions/no_read.txt')
        cls._set_rights('permissions/no_read.txt', read=False)
        cls._make_file('permissions/no_exec.txt')
        cls._set_rights('permissions/no_exec.txt', execute=False)

    def test_permissions_non_recursive(self):
        self._test_file_scanner(
            base_path=u'permissions',
            recursive=False,
            expected_result=(
                ('DIR', u'no_exec_dir'),
                ('DIR', u'no_read_dir'),
                ('DIR', u'normal_dir'),
                ('FILE', u'no_exec.txt'),
                ('FILE', u'no_read.txt'),
                ('FILE', u'normal.txt'),
            )
        )

    def test_permissions_recursive(self):
        self._test_file_scanner(
            base_path=u'permissions',
            recursive=True,
            expected_result=(
                ('FILE', u'no_exec_dir/file31.txt'),
                ('FILE', u'no_exec_dir/file32.txt'),
                ('DIR', u'no_read_dir', ('CannotExploreDirectoryException',)),
                ('FILE', u'normal_dir/file11.txt'),
                ('FILE', u'normal_dir/file12.txt'),
                ('FILE', u'no_exec.txt'),
                ('FILE', u'no_read.txt'),
                ('FILE', u'normal.txt'),
            )
        )

    def test_scan_non_existent(self):
        with self.assertRaises(BasePathDoesNotExistException):
            scan_files(os.path.join(self._test_dir_path, 'non_existent'))

    def test_scan_not_a_file(self):
        with self.assertRaises(BasePathIsNotADirectoryException):
            scan_files(os.path.join(self._test_dir_path, 'basic/file1'))

    def test_scan_cannot_explore(self):
        with self.assertRaises(CannotExploreBasePathException):
            scan_files(os.path.join(self._test_dir_path, 'permissions/no_read_dir'))

    def test_reports_progress(self):
        progress_events = []
        scan_files(
            os.path.join(self._test_dir_path, 'basic'),
            recursive=True,
            on_progress=self._progress_collector(progress_events)
        )

        self._verify_reported_progress(progress_events)

    def _test_file_scanner(self, base_path=u'', expected_result=None, **options):
        files = scan_files(os.path.join(self._test_dir_path, base_path), **options)

        self.assertEqual(
            tuple(f.test_repr() for f in files),
            expected_result
        )
