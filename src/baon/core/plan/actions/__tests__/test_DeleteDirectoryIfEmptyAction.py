# baon/core/plan/actions/__tests__/test_DeleteDirectoryIfEmptyAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.plan.actions.__tests__.RenamePlanActionTestCase import RenamePlanActionTestCase
from baon.core.plan.actions.__errors__.plan_action_errors import CannotDeleteDirDoesNotExistError,\
    CannotDeleteDirIsAFileError, CannotDeleteDirNoPermissionsError

from baon.core.plan.actions.DeleteDirectoryIfEmptyAction import DeleteDirectoryIfEmptyAction


class TestDeleteDirectoryIfEmptyAction(RenamePlanActionTestCase):

    def test_basic_empty(self):
        self.make_dir('empty_dir')

        self._make_action('empty_dir').execute()

        self.assert_path_does_not_exist('empty_dir')

    def test_basic_non_empty(self):
        self.make_file('non_empty_dir/file')

        self._make_action('non_empty_dir').execute()

        self.assert_is_dir('non_empty_dir')

    def test_fail_does_not_exist(self):
        with self.assertRaises(CannotDeleteDirDoesNotExistError):
            self._make_action('non_existent_dir').execute()

    def test_fail_is_a_file(self):
        self.make_file('file')

        with self.assertRaises(CannotDeleteDirIsAFileError):
            self._make_action('file').execute()

    def test_fail_no_write(self):
        self.make_file_structure('', (
            ('DIR', 'parent_dir', {'write': False}),
            ('DIR', 'parent_dir/empty_dir'),
        ))
        with self.assertRaises(CannotDeleteDirNoPermissionsError):
            self._make_action('parent_dir/empty_dir').execute()

    def test_fail_no_write_but_ok(self):
        self.make_file_structure('', (
            ('DIR', 'parent_dir', {'write': False}),
            ('FILE', 'parent_dir/non_empty_dir/file'),
        ))
        self._make_action('parent_dir/non_empty_dir').execute()

    def test_fail_no_read(self):
        self.make_dir('opaque_dir', read=False)

        with self.assertRaises(CannotDeleteDirNoPermissionsError):
            self._make_action('opaque_dir').execute()

    def test_undo(self):
        self.make_dir('empty_dir')

        action = self._make_action('empty_dir')

        action.execute()
        self.assert_path_does_not_exist('empty_dir')

        self.assertTrue(action.undo(), 'action.undo() failed unexpectedly')
        self.assert_is_dir('empty_dir')

    def test_undo_non_empty_ok(self):
        self.make_file('non_empty_dir/file')

        action = self._make_action('non_empty_dir')

        action.execute()
        self.assert_is_dir('non_empty_dir')

        self.assertTrue(action.undo(), 'action.undo() failed unexpectedly')
        self.assert_is_dir('non_empty_dir')

    def test_fail_undo(self):
        self.make_file('file')

        action = self._make_action('file')
        self.assertFalse(action.undo(), 'action.undo() succeeded unexpectedly')

    def _make_action(self, path):
        return DeleteDirectoryIfEmptyAction(self.resolve_test_path(path))
