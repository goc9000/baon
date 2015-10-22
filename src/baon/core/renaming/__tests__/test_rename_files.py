# baon/core/renaming/__tests__/test_rename_files.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.__tests__.abort_test_utils import abort_after_n_calls

from baon.core.renaming.__tests__.RenameFilesTestCase import RenameFilesTestCase
from baon.core.renaming.__errors__.rename_files_errors import RenameFilesAbortedError


class TestRenameFiles(RenameFilesTestCase):

    def test_basic(self):
        self._test_rename_files(
            input_description=(
                ('DIR', 'dir1'),
                ('DIR', 'dir2'),
                ('FILE', 'file1'),
                ('FILE', 'file2'),
                ('FILE', 'file3'),
            ),
            rules_text='..->paras',
            expected_result=(
                ('DIR', '(dir1)'),
                ('DIR', '(dir2)'),
                ('FILE', '(file1)'),
                ('FILE', '(file2)'),
                ('FILE', '(file3)'),
            ),
        )

    def test_no_use_extension(self):
        self._test_rename_files(
            input_description=(
                ('DIR', 'dir1'),
                ('DIR', 'dir2.d'),
                ('FILE', 'file1.txt'),
                ('FILE', 'file2.txt'),
                ('FILE', 'file3'),
            ),
            rules_text='..->paras',
            expected_result=(
                ('DIR', '(dir1)'),
                ('DIR', '(dir2.d)'),  # Directories always include the extension
                ('FILE', '(file1).txt'),
                ('FILE', '(file2).txt'),
                ('FILE', '(file3)'),
            ),
            use_extension=False,
        )

    def test_use_extension(self):
        self._test_rename_files(
            input_description=(
                ('DIR', 'dir1'),
                ('DIR', 'dir2.d'),
                ('FILE', 'file1.txt'),
                ('FILE', 'file2.txt'),
                ('FILE', 'file3'),
            ),
            rules_text='..->paras',
            expected_result=(
                ('DIR', '(dir1)'),
                ('DIR', '(dir2.d)'),
                ('FILE', '(file1.txt)'),
                ('FILE', '(file2.txt)'),
                ('FILE', '(file3)'),
            ),
            use_extension=True,
        )

    def test_no_use_path(self):
        self._test_rename_files(
            input_description=(
                ('FILE', 'dir1/file11.txt'),
                ('FILE', 'dir2.d/dir21/file211'),
                ('FILE', 'file1.txt'),
                ('FILE', 'file2.txt'),
                ('FILE', 'file3'),
            ),
            rules_text='..->paras',
            expected_result=(
                ('FILE', 'dir1/(file11).txt'),
                ('FILE', 'dir2.d/dir21/(file211)'),
                ('FILE', '(file1).txt'),
                ('FILE', '(file2).txt'),
                ('FILE', '(file3)'),
            ),
            use_path=False,
        )

    def test_use_path(self):
        self._test_rename_files(
            input_description=(
                ('FILE', 'dir1/file11.txt'),
                ('FILE', 'dir2.d/dir21/file211'),
                ('FILE', 'file1.txt'),
                ('FILE', 'file2.txt'),
                ('FILE', 'file3'),
            ),
            rules_text='..->paras',
            expected_result=(
                ('FILE', '(dir1/file11).txt'),
                ('FILE', '(dir2.d/dir21/file211)'),
                ('FILE', '(file1).txt'),
                ('FILE', '(file2).txt'),
                ('FILE', '(file3)'),
            ),
            use_path=True,
        )

    def test_override(self):
        self._test_rename_files(
            input_description=(
                ('FILE', 'dir1/file11.txt'),
                ('FILE', 'dir2.d/dir21/file211'),
                ('FILE', 'file1.txt'),
                ('FILE', 'file2.txt'),
                ('FILE', 'file3'),
            ),
            rules_text='..->paras',
            expected_result=(
                ('FILE', 'dir3/dir4/[file341].bin', 'OVERRIDE'),
                ('FILE', 'dir2.d/dir21/(file211)'),
                ('FILE', 'file100.txt', 'OVERRIDE'),
                ('FILE', '(file2).txt'),
                ('FILE', '(file3)'),
            ),
            use_path=False,
            overrides={
                'file1.txt': 'file100.txt',
                'dir1/file11.txt': 'dir3/dir4/[file341].bin',
            },
        )

    def test_reports_progress(self):
        with self.verify_reported_progress() as on_progress:
            self._test_rename_files(
                input_description=(('FILE', 'file{0}.txt'.format(i)) for i in range(10)),
                rules_text='"file" <<"0"',
                expected_result=tuple(('FILE', 'file0{0}.txt'.format(i)) for i in range(10)),
                on_progress=on_progress,
            )

    def test_abort(self):
        with self.assertRaises(RenameFilesAbortedError):
            self._test_rename_files(
                input_description=(('FILE', 'file{0}.txt'.format(i)) for i in range(10)),
                rules_text='"file" <<"0"',
                expected_result=tuple(('FILE', 'file0{0}.txt'.format(i)) for i in range(10)),
                check_abort=abort_after_n_calls(5),
            )
