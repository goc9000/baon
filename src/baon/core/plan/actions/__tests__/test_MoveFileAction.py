# baon/core/plan/actions/__tests__/test_MoveFileAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.plan.actions.__tests__.RenamePlanActionTestCase import RenamePlanActionTestCase
from baon.core.plan.actions.plan_action_exceptions import CannotMoveFileDoesNotExistException,\
    CannotMoveFileDestinationExistsException, CannotMoveFileNoPermissionsException
from baon.core.plan.actions.MoveFileAction import MoveFileAction


class TestMoveFileAction(RenamePlanActionTestCase):

    def test_basic(self):
        with self._temp_file_structure('', (('FILE', 'file1'),)):
            path1 = self._full_test_path('file1')
            path2 = self._full_test_path('file2')

            MoveFileAction(path1, path2).execute()

            self.assert_path_does_not_exist(path1)
            self.assert_is_file(path2)

    def test_basic_dir(self):
        with self._temp_file_structure('', (('DIR', 'dir1'),)):
            path1 = self._full_test_path('dir1')
            path2 = self._full_test_path('dir2')

            MoveFileAction(path1, path2).execute()

            self.assert_path_does_not_exist(path1)
            self.assert_is_dir(path2)

    def test_dir_with_files(self):
        with self._temp_file_structure('', (('FILE', 'dir1/file'),)):
            path1 = self._full_test_path('dir1')
            path2 = self._full_test_path('dir2')

            MoveFileAction(path1, path2).execute()

            self.assert_path_does_not_exist(path1)
            self.assert_is_dir(path2)
            self.assert_is_file(self._full_test_path('dir2/file'))

    def test_fail_not_exists(self):
        with self._temp_file_structure('', ()):
            with self.assertRaises(CannotMoveFileDoesNotExistException):
                MoveFileAction(self._full_test_path('file1'), self._full_test_path('file2')).execute()

    def test_fail_destination_exists(self):
        with self._temp_file_structure('', (
            ('FILE', 'file1'),
            ('FILE', 'file2'),
        )):
            with self.assertRaises(CannotMoveFileDestinationExistsException):
                MoveFileAction(self._full_test_path('file1'), self._full_test_path('file2')).execute()

    def test_no_source_permission(self):
        with self._temp_file_structure('', (
            ('FILE', 'dir1/file'),
            ('DIR', 'dir1', {'write': False}),
            ('DIR', 'dir2'),
        )):
            with self.assertRaises(CannotMoveFileNoPermissionsException):
                MoveFileAction(self._full_test_path('dir1/file'), self._full_test_path('dir2/file')).execute()

    def test_no_destination_permission(self):
        with self._temp_file_structure('', (
            ('FILE', 'dir1/file'),
            ('DIR', 'dir2', {'write': False}),
        )):
            with self.assertRaises(CannotMoveFileNoPermissionsException):
                MoveFileAction(self._full_test_path('dir1/file'), self._full_test_path('dir2/file')).execute()

    def test_undo(self):
        with self._temp_file_structure('', (('FILE', 'file1'),)):
            path1 = self._full_test_path('file1')
            path2 = self._full_test_path('file2')
            action = MoveFileAction(path1, path2)

            action.execute()
            self.assert_path_does_not_exist(path1)
            self.assert_is_file(path2)

            self.assertTrue(action.undo(), 'action.undo() failed unexpectedly')
            self.assert_is_file(path1)
            self.assert_path_does_not_exist(path2)

    def test_undo_fail(self):
        with self._temp_file_structure('', (('FILE', 'file1'),)):
            path1 = self._full_test_path('file1')
            path2 = self._full_test_path('file2')
            action = MoveFileAction(path1, path2)

            self.assertFalse(action.undo(), 'action.undo() succeeded unexpectedly')
            self.assert_is_file(path1)
            self.assert_path_does_not_exist(path2)
