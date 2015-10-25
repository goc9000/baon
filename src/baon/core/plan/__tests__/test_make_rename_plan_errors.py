# baon/core/plan/__tests__/test_make_rename_plan_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.plan.__tests__.MakeRenamePlanTestCaseBase import MakeRenamePlanTestCaseBase


class TestMakeRenamePlanErrors(MakeRenamePlanTestCaseBase):

    def test_file_in_way_will_not_move(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file1'),
                ('FILE', 'file2'),
                ('FILE', 'entry'),
            ),
            '"file2"->"entry/file"',
            ('CannotCreateDestinationDirFileInTheWayWillNotMoveError', {'destination_dir': 'entry'}),
            filter_scanned_files=lambda file_ref: file_ref.path.basename() != 'entry')

    def test_fail_if_renamed_files_have_errors(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file1'),
                ('FILE', 'file2'),
            ),
            '"file2"->"file1"',
            ('RenamedFilesListHasErrorsError',))

    def test_ok_if_renamed_files_have_warnings(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file1'),
                ('FILE', 'file2'),
            ),
            '"file2"->"file  2"',
            (
                ('MoveFile', 'file2', 'file  2'),
            ))
