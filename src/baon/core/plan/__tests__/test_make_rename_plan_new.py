# baon/core/plan/__tests__/test_make_rename_plan_new.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.plan.__tests__.MakeRenamePlanNewTestCaseBase import MakeRenamePlanNewTestCaseBase


class TestMakeRenamePlan(MakeRenamePlanNewTestCaseBase):

    def test_trivial(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'old_file', 'new_file'),
            ),
            (
                ('CreateDirectory', '<STAGING_DIR>'),
                # TODO: complete test
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
                # TODO: complete test
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
