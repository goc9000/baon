# baon/core/plan/actions/__tests__/test_CreateDirectoryAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.plan.actions.__tests__.RenamePlanActionTestCase import RenamePlanActionTestCase
from baon.core.plan.actions.plan_action_exceptions import CannotCreateDirAlreadyExistsException, \
    CannotCreateDirFileInWayException, CannotCreateDirParentDoesNotExistException, \
    CannotCreateDirParentNotADirectoryException, CannotCreateDirNoPermissionsException
from baon.core.plan.actions.CreateDirectoryAction import CreateDirectoryAction


class TestCreateDirectoryAction(RenamePlanActionTestCase):

    def test_basic(self):
        with self._temp_file_structure('', ()):
            path = self._full_test_path('created_dir')

            CreateDirectoryAction(path).execute()

            self.assert_is_dir(path)

    def test_fail_already_exists(self):
        with self._temp_file_structure('', (('DIR', 'existing_dir'),)):
            with self.assertRaises(CannotCreateDirAlreadyExistsException):
                CreateDirectoryAction(self._full_test_path('existing_dir')).execute()

    def test_fail_file_in_way(self):
        with self._temp_file_structure('', (('FILE', 'existing_file'),)):
            with self.assertRaises(CannotCreateDirFileInWayException):
                CreateDirectoryAction(self._full_test_path('existing_file')).execute()

    def test_fail_no_parent(self):
        with self._temp_file_structure('', ()):
            with self.assertRaises(CannotCreateDirParentDoesNotExistException):
                CreateDirectoryAction(self._full_test_path('parent/new_dir')).execute()

    def test_fail_parent_is_file(self):
        with self._temp_file_structure('', (('FILE', 'parent'),)):
            with self.assertRaises(CannotCreateDirParentNotADirectoryException):
                CreateDirectoryAction(self._full_test_path('parent/new_dir')).execute()

    def test_fail_parent_permissions(self):
        with self._temp_file_structure('', (('DIR', 'parent', {'write': False}),)):
            with self.assertRaises(CannotCreateDirNoPermissionsException):
                CreateDirectoryAction(self._full_test_path('parent/new_dir')).execute()

    def test_undo(self):
        with self._temp_file_structure('', ()):
            path = self._full_test_path('test_dir')
            action = CreateDirectoryAction(path)

            action.execute()
            self.assert_is_dir(path)

            self.assertTrue(action.undo(), 'action.undo() failed unexpectedly')
            self.assert_path_does_not_exist(path)

    def test_fail_undo(self):
        with self._temp_file_structure('', ()):
            action = CreateDirectoryAction(self._full_test_path('test_dir'))
            self.assertFalse(action.undo(), 'action.undo() succeeded unexpectedly')
