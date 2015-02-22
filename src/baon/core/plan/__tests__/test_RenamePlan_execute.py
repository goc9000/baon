# baon/core/plan/__tests__/test_RenamePlan_execute.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.__tests__.FileSystemTestCase import FileSystemTestCase

from baon.core.plan.__tests__.RenamePlanTestCaseBase import RenamePlanTestCaseBase

from baon.core.plan.__errors__.rename_plan_errors import RenamePlanExecuteFailedBecauseActionFailedError

from baon.core.files.scan_files import scan_files

from baon.core.plan.RenamePlan import RenamePlan
from baon.core.plan.actions.CreateDirectoryAction import CreateDirectoryAction
from baon.core.plan.actions.MoveFileAction import MoveFileAction
from baon.core.plan.actions.DeleteDirectoryIfEmptyAction import DeleteDirectoryIfEmptyAction


class TestRenamePlanExecute(RenamePlanTestCaseBase, FileSystemTestCase):

    INITIAL_FILE_STRUCTURE = (
        ('FILE', 'dir1/file1'),
        ('FILE', 'file2'),
        ('FILE', 'file3')
    )

    FINAL_FILE_STRUCTURE = (
        ('FILE', 'dir3/file03'),
        ('FILE', 'file01'),
        ('FILE', 'file02'),
    )

    def setUp(self):
        super(TestRenamePlanExecute, self).setUp()

        self.make_file_structure('', self.INITIAL_FILE_STRUCTURE)

    def test_execute_success(self):
        self._make_rename_plan().execute()

        self.assertEqual(self._rescan_files(), self.FINAL_FILE_STRUCTURE)

    def test_execute_failed(self):
        # Let's say an app already created this conflicting entry in the meantime
        self.make_file('file02')
        actual_initial_structure = self._rescan_files()

        with self.assertRaises(RenamePlanExecuteFailedBecauseActionFailedError) as e:
            self._make_rename_plan().execute()

        # Files should have been rolled back
        self.assertEqual(self._rescan_files(), actual_initial_structure)

    def _make_rename_plan(self):
        return RenamePlan([
            CreateDirectoryAction(self.resolve_test_path('dir3')),
            MoveFileAction(self.resolve_test_path('dir1/file1'), self.resolve_test_path('file01')),
            MoveFileAction(self.resolve_test_path('file2'), self.resolve_test_path('file02')),
            MoveFileAction(self.resolve_test_path('file3'), self.resolve_test_path('dir3/file03')),
            DeleteDirectoryIfEmptyAction(self.resolve_test_path('dir1')),
        ])

    def _rescan_files(self):
        return tuple(f.test_repr() for f in scan_files(self.resolve_test_path(''), recursive=True))
