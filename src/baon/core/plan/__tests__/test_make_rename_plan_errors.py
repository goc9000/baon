# baon/core/plan/__tests__/test_make_rename_plan_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.plan.__tests__.MakeRenamePlanTestCaseBase import MakeRenamePlanTestCaseBase


class TestMakeRenamePlanErrors(MakeRenamePlanTestCaseBase):

    def test_base_path_does_not_exist(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'dummy', 'dummy_renamed'),
            ),
            actual_files=(),
            base_path_override='non_existent',
            expected_result=('BasePathNotFoundError', {'base_path': 'non_existent'}),
        )

    def test_base_path_not_a_dir(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'dummy', 'dummy_renamed'),
            ),
            actual_files=(
                ('FILE', 'not_a_dir'),
            ),
            base_path_override='not_a_dir',
            expected_result=('BasePathNotADirError', {'base_path': 'not_a_dir'}),
        )

    def test_base_path_no_permissions(self):
        for permission in ['read', 'write', 'execute']:
            with self.subTest(missing_permission=permission):
                self._test_make_rename_plan(
                    (
                        ('FILE', 'dummy', 'dummy_renamed'),
                    ),
                    actual_files=(
                        ('DIR', 'locked', {permission: False}),
                        ('FILE', 'locked/dummy'),
                    ),
                    base_path_override='locked',
                    expected_result=('NoPermissionsForBasePathError', {'base_path': 'locked'}),
                )

    def test_file_in_way_will_not_move(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file1'),
                ('FILE', 'file2', 'entry/file'),
            ),
            ('CannotCreateDestinationDirFileInTheWayWillNotMoveError', {'destination_dir': 'entry'}),
            actual_files=(
                ('FILE', 'file1'),
                ('FILE', 'file2'),
                ('FILE', 'entry'),
            ),
        )

    def test_fail_if_renamed_files_have_errors(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file1'),
                ('FILE', 'file2', 'file1', ('SyntheticFileError',)),
            ),
            ('RenamedFilesListHasErrorsError',),
        )

    def test_ok_if_renamed_files_have_warnings(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file1'),
                ('FILE', 'file2', 'file  2', ('SyntheticFileWarning',)),
            ),
            (
                ('MoveFile', 'file2', 'file  2'),
            ),
        )
