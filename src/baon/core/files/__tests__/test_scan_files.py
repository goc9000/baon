# baon/core/files/__tests__/test_scan_files.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.__tests__.FileSystemTestCase import FileSystemTestCase, requires_links_support, requires_unicode_support

from baon.core.utils.progress.ReportsProgressTestCase import ReportsProgressTestCase

from baon.core.files.__errors__.scan_files_errors import BasePathDoesNotExistError, BasePathIsNotADirectoryError,\
    CannotExploreBasePathError

from baon.core.files.scan_files import scan_files


class TestScanFiles(FileSystemTestCase, ReportsProgressTestCase):

    BASIC_FILE_STRUCTURE = (
        ('FILE', 'dir1/file11.txt'),
        ('FILE', 'dir1/file12'),
        ('FILE', 'dir2/dir21/file211'),
        ('FILE', 'dir2/dir21/file212'),
        ('FILE', 'dir2/dir22/file221.bin'),
        ('FILE', 'dir2/file21'),
        ('DIR', 'dir3/dir31'),
        ('FILE', 'dir3/dir32/file321.txt'),
        ('FILE', 'file1'),
        ('FILE', 'file2.bin'),
        ('FILE', 'file3'),
    )

    def test_basic_non_recursive(self):
        self._test_scan_files(
            setup_files=self.BASIC_FILE_STRUCTURE,
            recursive=False,
            expected_result=(
                ('DIR', 'dir1'),
                ('DIR', 'dir2'),
                ('DIR', 'dir3'),
                ('FILE', 'file1'),
                ('FILE', 'file2.bin'),
                ('FILE', 'file3'),
            )
        )

    def test_basic_recursive(self):
        self._test_scan_files(
            setup_files=self.BASIC_FILE_STRUCTURE,
            recursive=True,
            expected_result=(
                ('FILE', 'dir1/file11.txt'),
                ('FILE', 'dir1/file12'),
                ('FILE', 'dir2/dir21/file211'),
                ('FILE', 'dir2/dir21/file212'),
                ('FILE', 'dir2/dir22/file221.bin'),
                ('FILE', 'dir2/file21'),
                ('FILE', 'dir3/dir32/file321.txt'),
                ('FILE', 'file1'),
                ('FILE', 'file2.bin'),
                ('FILE', 'file3'),
            )
        )

    EMPTIES_FILE_STRUCTURE = (
        ('DIR', 'empty'),
        ('DIR', 'dir1/empty1'),
        ('FILE', 'dir1/file1'),
    )

    def test_empty_dirs_non_recursive(self):
        self._test_scan_files(
            setup_files=self.EMPTIES_FILE_STRUCTURE,
            recursive=False,
            expected_result=(
                ('DIR', 'dir1'),
                ('DIR', 'empty'),
            )
        )

    def test_empty_dirs_recursive(self):
        self._test_scan_files(
            setup_files=self.EMPTIES_FILE_STRUCTURE,
            recursive=True,
            expected_result=(
                ('FILE', 'dir1/file1'),
            )
        )

    LINKS_FILE_STRUCTURE = (
        ('FILE', 'file2.bin'),
        ('DIR', 'dir1'),
        ('LINK', 'link1', 'file2.bin'),
        ('LINK', 'link2', 'dir1'),
        ('LINK', 'link3', 'dangling'),
        ('LINK', 'link4', 'link2'),
    )

    @requires_links_support
    def test_links_non_recursive(self):
        self._test_scan_files(
            setup_files=self.LINKS_FILE_STRUCTURE,
            recursive=False,
            expected_result=(
                ('DIR', 'dir1'),
                ('LINK:DIR', 'link2'),
                ('LINK:DIR', 'link4'),
                ('FILE', 'file2.bin'),
                ('LINK:FILE', 'link1'),
                ('LINK:FILE', 'link3'),
            )
        )

    @requires_links_support
    def test_links_recursive(self):
        self._test_scan_files(
            setup_files=self.LINKS_FILE_STRUCTURE,
            recursive=True,
            expected_result=(
                ('LINK:DIR', 'link2'),  # Symlinks are not followed even in recursive mode
                ('LINK:DIR', 'link4'),
                ('FILE', 'file2.bin'),
                ('LINK:FILE', 'link1'),
                ('LINK:FILE', 'link3'),
            )
        )

    UNICODE_FILE_STRUCTURE = (
        ('FILE', '\u0111\u0131\u0157/\u0192\u00ef\u0142\u00e9\u2461.txt'),
        ('FILE', '\u0192\u00ef\u0142\u00e9\u2460.txt'),
    )

    @requires_unicode_support
    def test_unicode_non_recursive(self):
        self._test_scan_files(
            setup_files=self.UNICODE_FILE_STRUCTURE,
            recursive=False,
            expected_result=(
                ('DIR', '\u0111\u0131r\u0327'),
                ('FILE', '\u0192i\u0308\u0142e\u0301\u2460.txt'),
            )
        )

    @requires_unicode_support
    def test_unicode_recursive(self):
        self._test_scan_files(
            setup_files=self.UNICODE_FILE_STRUCTURE,
            recursive=True,
            expected_result=(
                ('FILE', '\u0111\u0131r\u0327/\u0192i\u0308\u0142e\u0301\u2461.txt'),
                ('FILE', '\u0192i\u0308\u0142e\u0301\u2460.txt'),
            )
        )

    PERMISSIONS_FILE_STRUCTURE = (
        ('FILE', 'normal_dir/file11.txt'),
        ('FILE', 'normal_dir/file12.txt'),
        ('DIR', 'no_read_dir', {'read': False}),
        ('FILE', 'no_read_dir/file21.txt'),
        ('FILE', 'no_read_dir/file22.txt'),
        ('DIR', 'no_exec_dir', {'execute': False}),
        ('FILE', 'no_exec_dir/file31.txt'),
        ('FILE', 'no_exec_dir/file32.txt'),
        ('FILE', 'normal.txt'),
        ('FILE', 'no_read.txt', {'read': False}),
        ('FILE', 'no_exec.txt', {'execute': False}),
    )

    def test_permissions_non_recursive(self):
        self._test_scan_files(
            setup_files=self.PERMISSIONS_FILE_STRUCTURE,
            recursive=False,
            expected_result=(
                ('DIR', 'no_exec_dir'),
                ('DIR', 'no_read_dir'),
                ('DIR', 'normal_dir'),
                ('FILE', 'no_exec.txt'),
                ('FILE', 'no_read.txt'),
                ('FILE', 'normal.txt'),
            )
        )

    def test_permissions_recursive(self):
        self._test_scan_files(
            setup_files=self.PERMISSIONS_FILE_STRUCTURE,
            recursive=True,
            expected_result=(
                ('FILE', 'no_exec_dir/file31.txt'),
                ('FILE', 'no_exec_dir/file32.txt'),
                ('DIR', 'no_read_dir', ('CannotExploreDirectoryError',)),
                ('FILE', 'normal_dir/file11.txt'),
                ('FILE', 'normal_dir/file12.txt'),
                ('FILE', 'no_exec.txt'),
                ('FILE', 'no_read.txt'),
                ('FILE', 'normal.txt'),
            )
        )

    def test_scan_non_existent(self):
        with self.assertRaises(BasePathDoesNotExistError):
            scan_files(self.resolve_test_path('non_existent'))

    def test_scan_base_path_not_a_dir(self):
        with self.assertRaises(BasePathIsNotADirectoryError):
            with self.temp_file_structure('', (
                ('FILE', 'file1'),
            )):
                scan_files(self.resolve_test_path('file1'))

    def test_scan_cannot_explore(self):
        with self.assertRaises(CannotExploreBasePathError):
            with self.temp_file_structure('', (
                ('DIR', 'no_read_dir', {'read': False}),
            )):
                scan_files(self.resolve_test_path('no_read_dir'))

    def test_reports_progress(self):
        with self.verify_reported_progress() as progress_receiver:
            with self.temp_file_structure('', self.BASIC_FILE_STRUCTURE):
                scan_files(
                    base_path=self.resolve_test_path(''),
                    recursive=True,
                    progress_receiver=progress_receiver,
                )

    def _test_scan_files(self, setup_files=None, expected_result=None, **options):
        with self.temp_file_structure('', setup_files):
            files = scan_files(self.resolve_test_path(''), **options)

        self.assertEqual(
            tuple(f.test_repr() for f in files),
            expected_result,
        )
