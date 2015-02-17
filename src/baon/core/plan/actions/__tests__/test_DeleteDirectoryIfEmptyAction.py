# baon/core/plan/actions/__tests__/test_DeleteDirectoryIfEmptyAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.plan.actions.__tests__.RenamePlanActionTestCase import RenamePlanActionTestCase
from baon.core.plan.actions.plan_action_exceptions import CannotDeleteDirDoesNotExistException,\
    CannotDeleteDirIsAFileException, CannotDeleteDirNoPermissionsException
from baon.core.plan.actions.DeleteDirectoryIfEmptyAction import DeleteDirectoryIfEmptyAction


class TestDeleteDirectoryIfEmptyAction(RenamePlanActionTestCase):

    def test_basic_empty(self):
        self.make_dir('empty_dir')

        path = self.full_test_path('empty_dir')

        DeleteDirectoryIfEmptyAction(path).execute()

        self.assert_path_does_not_exist(path)

    def test_basic_non_empty(self):
        self.make_file('non_empty_dir/file')

        path = self.full_test_path('non_empty_dir')

        DeleteDirectoryIfEmptyAction(path).execute()

        self.assert_is_dir(path)

    def test_fail_does_not_exist(self):
        with self.assertRaises(CannotDeleteDirDoesNotExistException):
            DeleteDirectoryIfEmptyAction(self.full_test_path('non_existent_dir')).execute()

    def test_fail_is_a_file(self):
        self.make_file('file')

        with self.assertRaises(CannotDeleteDirIsAFileException):
            DeleteDirectoryIfEmptyAction(self.full_test_path('file')).execute()

    def test_fail_no_write(self):
        self.realize_file_structure('', (
            ('DIR', 'parent_dir', {'write': False}),
            ('DIR', 'parent_dir/empty_dir'),
        ))
        with self.assertRaises(CannotDeleteDirNoPermissionsException):
            DeleteDirectoryIfEmptyAction(self.full_test_path('parent_dir/empty_dir')).execute()

    def test_fail_no_write_but_ok(self):
        self.realize_file_structure('', (
            ('DIR', 'parent_dir', {'write': False}),
            ('FILE', 'parent_dir/non_empty_dir/file'),
        ))
        DeleteDirectoryIfEmptyAction(self.full_test_path('parent_dir/non_empty_dir')).execute()

    def test_fail_no_read(self):
        self.realize_file_structure('', (('DIR', 'opaque_dir', {'read': False}),))

        with self.assertRaises(CannotDeleteDirNoPermissionsException):
            DeleteDirectoryIfEmptyAction(self.full_test_path('opaque_dir')).execute()

    def test_undo(self):
        self.make_dir('empty_dir')

        path = self.full_test_path('empty_dir')
        action = DeleteDirectoryIfEmptyAction(path)

        action.execute()
        self.assert_path_does_not_exist(path)

        self.assertTrue(action.undo(), 'action.undo() failed unexpectedly')
        self.assert_is_dir(path)

    def test_undo_non_empty_ok(self):
        self.make_file('non_empty_dir/file')

        path = self.full_test_path('non_empty_dir')
        action = DeleteDirectoryIfEmptyAction(path)

        action.execute()
        self.assert_is_dir(path)

        self.assertTrue(action.undo(), 'action.undo() failed unexpectedly')
        self.assert_is_dir(path)

    def test_fail_undo(self):
        self.make_file('file')

        action = DeleteDirectoryIfEmptyAction(self.full_test_path('file'))
        self.assertFalse(action.undo(), 'action.undo() succeeded unexpectedly')
