# baon/core/plan/__tests__/test_make_rename_plan.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.plan.__tests__.MakeRenamePlanTestCaseBase import MakeRenamePlanTestCaseBase


class TestMakeRenamePlan(MakeRenamePlanTestCaseBase):

    def test_trivial(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'old_file', 'new_file'),
            ),
            (
                ('CreateDirectory', '<STAGING_DIR>'),
                ('MoveFile', 'old_file', '<STAGING_DIR>/new_file'),
                ('MoveFile', '<STAGING_DIR>/new_file', 'new_file'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>'),
            ),
        )

    def test_complex(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'dir1/file11.txt', 'dir1/file41.txt'),
                ('FILE', 'dir1/file12', 'dir1/dir3/file42'),
                ('FILE', 'dir2/dir21/file211'),
                ('FILE', 'dir2/file21'),
                ('FILE', 'file1', 'file4'),
                ('FILE', 'file2.bin'),
            ),
            (
                ('CreateDirectory', '<STAGING_DIR>'),
                ('CreateDirectory', '<STAGING_DIR>/dir1'),
                ('CreateDirectory', '<STAGING_DIR>/dir1/dir3'),
                ('MoveFile', 'dir1/file11.txt', '<STAGING_DIR>/dir1/file41.txt'),
                ('MoveFile', 'dir1/file12', '<STAGING_DIR>/dir1/dir3/file42'),
                ('MoveFile', 'file1', '<STAGING_DIR>/file4'),
                ('DeleteEmptyDirectory', 'dir1'),
                ('CreateDirectory', 'dir1'),
                ('CreateDirectory', 'dir1/dir3'),
                ('MoveFile', '<STAGING_DIR>/dir1/file41.txt', 'dir1/file41.txt'),
                ('MoveFile', '<STAGING_DIR>/dir1/dir3/file42', 'dir1/dir3/file42'),
                ('MoveFile', '<STAGING_DIR>/file4', 'file4'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>/dir1/dir3'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>/dir1'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>'),
            ),
        )

    def test_empty_plan_if_no_files(self):
        self._test_make_rename_plan(
            (),
            (),
        )

    def test_empty_plan_if_no_changes(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'unchanged'),
            ),
            (),
        )

    def test_file_in_way_will_move(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file1'),
                ('FILE', 'file2', 'entry/file'),
                ('FILE', 'entry', 'moved'),
            ),
            (
                ('CreateDirectory', '<STAGING_DIR>'),
                ('CreateDirectory', '<STAGING_DIR>/entry'),
                ('MoveFile', 'file2', '<STAGING_DIR>/entry/file'),
                ('MoveFile', 'entry', '<STAGING_DIR>/moved'),
                ('CreateDirectory', 'entry'),
                ('MoveFile', '<STAGING_DIR>/entry/file', 'entry/file'),
                ('MoveFile', '<STAGING_DIR>/moved', 'moved'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>/entry'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>'),
            ),
        )

    def test_chain(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file1', 'file2'),
                ('FILE', 'file2', 'file3'),
                ('FILE', 'file3', 'file4'),
                ('FILE', 'file4', 'file5'),
            ),
            (
                ('CreateDirectory', '<STAGING_DIR>'),
                ('MoveFile', 'file1', '<STAGING_DIR>/file2'),
                ('MoveFile', 'file2', '<STAGING_DIR>/file3'),
                ('MoveFile', 'file3', '<STAGING_DIR>/file4'),
                ('MoveFile', 'file4', '<STAGING_DIR>/file5'),
                ('MoveFile', '<STAGING_DIR>/file2', 'file2'),
                ('MoveFile', '<STAGING_DIR>/file3', 'file3'),
                ('MoveFile', '<STAGING_DIR>/file4', 'file4'),
                ('MoveFile', '<STAGING_DIR>/file5', 'file5'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>'),
            ),
        )

    def test_circular(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file1', 'file2'),
                ('FILE', 'file2', 'file3'),
                ('FILE', 'file3', 'file4'),
                ('FILE', 'file4', 'file1'),
            ),
            (
                ('CreateDirectory', '<STAGING_DIR>'),
                ('MoveFile', 'file1', '<STAGING_DIR>/file2'),
                ('MoveFile', 'file2', '<STAGING_DIR>/file3'),
                ('MoveFile', 'file3', '<STAGING_DIR>/file4'),
                ('MoveFile', 'file4', '<STAGING_DIR>/file1'),
                ('MoveFile', '<STAGING_DIR>/file2', 'file2'),
                ('MoveFile', '<STAGING_DIR>/file3', 'file3'),
                ('MoveFile', '<STAGING_DIR>/file4', 'file4'),
                ('MoveFile', '<STAGING_DIR>/file1', 'file1'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>'),
            ),
        )

    def test_complex_permutation(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file1', 'file2'),
                ('FILE', 'file2', 'file10'),
                ('FILE', 'file3', 'file4'),
                ('FILE', 'file4', 'file5'),
                ('FILE', 'file5', 'file3'),
                ('FILE', 'file6', 'file7'),
                ('FILE', 'file7', 'file8'),
                ('FILE', 'file8', 'file9'),
            ),
            (
                ('CreateDirectory', '<STAGING_DIR>'),
                ('MoveFile', 'file1', '<STAGING_DIR>/file2'),
                ('MoveFile', 'file2', '<STAGING_DIR>/file10'),
                ('MoveFile', 'file3', '<STAGING_DIR>/file4'),
                ('MoveFile', 'file4', '<STAGING_DIR>/file5'),
                ('MoveFile', 'file5', '<STAGING_DIR>/file3'),
                ('MoveFile', 'file6', '<STAGING_DIR>/file7'),
                ('MoveFile', 'file7', '<STAGING_DIR>/file8'),
                ('MoveFile', 'file8', '<STAGING_DIR>/file9'),
                ('MoveFile', '<STAGING_DIR>/file2', 'file2'),
                ('MoveFile', '<STAGING_DIR>/file10', 'file10'),
                ('MoveFile', '<STAGING_DIR>/file4', 'file4'),
                ('MoveFile', '<STAGING_DIR>/file5', 'file5'),
                ('MoveFile', '<STAGING_DIR>/file3', 'file3'),
                ('MoveFile', '<STAGING_DIR>/file7', 'file7'),
                ('MoveFile', '<STAGING_DIR>/file8', 'file8'),
                ('MoveFile', '<STAGING_DIR>/file9', 'file9'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>'),
            ),
        )

    def test_staging_dir_already_exists(self):
        self._test_make_rename_plan(
            (
                ('DIR', '<STAGING_DIR>'),
                ('FILE', 'file', '<STAGING_DIR>/file'),
            ),
            (
                ('CreateDirectory', '<ALTERNATE_STAGING_DIR>'),
                ('CreateDirectory', '<ALTERNATE_STAGING_DIR>/<STAGING_DIR>'),
                ('MoveFile', 'file', '<ALTERNATE_STAGING_DIR>/<STAGING_DIR>/file'),
                ('MoveFile', '<ALTERNATE_STAGING_DIR>/<STAGING_DIR>/file', '<STAGING_DIR>/file'),
                ('DeleteEmptyDirectory', '<ALTERNATE_STAGING_DIR>/<STAGING_DIR>'),
                ('DeleteEmptyDirectory', '<ALTERNATE_STAGING_DIR>'),
            ),
        )
