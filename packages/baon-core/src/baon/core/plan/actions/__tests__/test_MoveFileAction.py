# baon/core/plan/actions/__tests__/test_MoveFileAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.__tests__.FileSystemTestCase import requires_permissions_support
from baon.core.plan.actions.MoveFileAction import MoveFileAction
from baon.core.plan.actions.__errors__.plan_action_errors import CannotMoveFileDoesNotExistError,\
    CannotMoveFileDestinationExistsError, CannotMoveFileNoPermissionsError
from baon.core.plan.actions.__tests__.RenamePlanActionTestCase import RenamePlanActionTestCase


class TestMoveFileAction(RenamePlanActionTestCase):

    def test_basic(self):
        self.make_file('file1')

        self._make_action('file1', 'file2').execute()

        self.assert_path_does_not_exist('file1')
        self.assert_is_file('file2')

    def test_basic_dir(self):
        self.make_dir('dir1')

        self._make_action('dir1', 'dir2').execute()

        self.assert_path_does_not_exist('dir1')
        self.assert_is_dir('dir2')

    def test_dir_with_files(self):
        self.make_file('dir1/file')

        self._make_action('dir1', 'dir2').execute()

        self.assert_path_does_not_exist('dir1')
        self.assert_is_dir('dir2')
        self.assert_is_file('dir2/file')

    def test_fail_not_exists(self):
        with self.assertRaises(CannotMoveFileDoesNotExistError):
            self._make_action('file1', 'file2').execute()

    def test_fail_destination_exists(self):
        self.make_file('file1')
        self.make_file('file2')

        with self.assertRaises(CannotMoveFileDestinationExistsError):
            self._make_action('file1', 'file2').execute()

    @requires_permissions_support
    def test_no_source_permission(self):
        self.make_file_structure('', (
            ('FILE', 'dir1/file'),
            ('DIR', 'dir1', '#nowrite'),
            ('DIR', 'dir2'),
        ))

        with self.assertRaises(CannotMoveFileNoPermissionsError):
            self._make_action('dir1/file', 'dir2/file').execute()

    @requires_permissions_support
    def test_no_destination_permission(self):
        self.make_file_structure('', (
            ('FILE', 'dir1/file'),
            ('DIR', 'dir2', '#nowrite'),
        ))

        with self.assertRaises(CannotMoveFileNoPermissionsError):
            self._make_action('dir1/file', 'dir2/file').execute()

    def test_undo(self):
        self.make_file('file1')

        action = self._make_action('file1', 'file2')

        action.execute()
        self.assert_path_does_not_exist('file1')
        self.assert_is_file('file2')

        self.assertTrue(action.undo(), 'action.undo() failed unexpectedly')
        self.assert_is_file('file1')
        self.assert_path_does_not_exist('file2')

    def test_undo_fail(self):
        self.make_file('file1')

        action = self._make_action('file1', 'file2')

        self.assertFalse(action.undo(), 'action.undo() succeeded unexpectedly')
        self.assert_is_file('file1')
        self.assert_path_does_not_exist('file2')

    def _make_action(self, from_path, to_path):
        return MoveFileAction(self.resolve_test_path(from_path), self.resolve_test_path(to_path))
