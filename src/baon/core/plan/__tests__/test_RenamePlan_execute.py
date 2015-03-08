# baon/core/plan/__tests__/test_RenamePlan_execute.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

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

    def test_undo_full(self):
        """
        This tests the undo() function for an entire plan, which is used if BAON crashes during the execution of a
        plan. A backup of the plan that was being executed is reloaded from disk upon startup, and we undo its actions
        so that the original state is restored.

        We first test the simplest case, when all the operations were executed successfully, and we somehow crashed
        right before reporting the results to the caller.
        """
        plan = self._make_rename_plan()
        plan.execute()

        self.assertTrue(plan.undo())

        self.assertEqual(self._rescan_files(), self.INITIAL_FILE_STRUCTURE)

    def test_undo_partial(self):
        """
        This tests the undo() function for the more likely case where the operations only succeeded up to a point.
        Although we do not know which of the operations was the last to be executed, we just attempt to execute all of
        the operations starting from the last. Thanks to the careful design of the operations, we can be certain that
        past a certain point, all the operations should start succeeding, assuming the state of the directory has not
        been altered in the time between the crash and BAON being restarted.

        We first test the simple case where the last executed operation is unambiguous and the directory state is
        intact since the crash.
        """
        plan = self._make_rename_plan()

        for i in range(3):
            plan.steps[i].execute()

        self.assertTrue(plan.undo_partial_execution())

        self.assertEqual(self._rescan_files(), self.INITIAL_FILE_STRUCTURE)

    def test_undo_partial_tampered(self):
        """
        This tests the undo() function if the directory's state has been tampered with. It needs to detect this so
        that we can report the problem to the user.
        """
        plan = self._make_rename_plan()

        for i in range(3):
            plan.steps[i].execute()

        # Tamper with the directory state
        os.remove(self.resolve_test_path('file01'))

        self.assertFalse(plan.undo_partial_execution())

    def test_undo_ambiguous(self):
        """
        This tests a complex case that results from the fact that DeleteDirectoryIfEmpty is a no-op if the directory
        is not empty, and thus it is not possible to determine whether the operation was executed or not. This can
        create problems in a scenario like:

        Op1: MoveFile (last executed)
        Op2: MoveFile (not executed)
        Op3: DeleteDirectoryIfEmpty for non-empty dir (no-op)
        Op4: DeleteDirectoryIfEmpty for empty dir (not executed)

        Regardless of whether we consider the undo() of Op3 to be a success or failure, we will have problems. If we
        consider it to be a success, then the state of the undo() operations will be:

        Op4: Fail
        Op3: Success
        Op2: Fail
        Op1: Success

        Thus, we will incorrectly consider Op3 to be the last executed operation (since it's the first undo operation
        that succeeded), then consider Op2's failure to be a sign that the directory's state has been tampered with
        and thus the entire undo() operation is a failure - which is not correct.

        Conversely, if Op3 is considered to be failed, then we will not correctly handle the situation where all
        operations actually succeeded. We will have:

        Op4: Success
        Op3: Fail
        Op2: Success
        Op1: Success

        Thus, we will again consider that the directory has been tampered with, when it really hasn't.

        The correct solution to this is to have a special status for no-ops (i.e. None) and ignore it when looking for
        the first undo() operation that succeeded, as well as any subsequent errors. This functionality is built into
        the plan-level undo() function, and is tested specifically by this test case.
        """
        plan = self._make_rename_plan()

        plan.steps[0].execute()

        # Now the success status for the undo() operations will be:
        # Op5: None
        # Op4: Fail
        # Op3: Fail
        # Op2: Fail
        # Op1: Success
        self.assertTrue(plan.undo_partial_execution())

        self.assertEqual(self._rescan_files(), self.INITIAL_FILE_STRUCTURE)

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
