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
        path = self.full_test_path('created_dir')

        CreateDirectoryAction(path).execute()

        self.assert_is_dir(path)

    def test_fail_already_exists(self):
        self.make_dir('existing_dir')

        with self.assertRaises(CannotCreateDirAlreadyExistsException):
            CreateDirectoryAction(self.full_test_path('existing_dir')).execute()

    def test_fail_file_in_way(self):
        self.make_file('existing_file')

        with self.assertRaises(CannotCreateDirFileInWayException):
            CreateDirectoryAction(self.full_test_path('existing_file')).execute()

    def test_fail_no_parent(self):
        with self.assertRaises(CannotCreateDirParentDoesNotExistException):
            CreateDirectoryAction(self.full_test_path('parent/new_dir')).execute()

    def test_fail_parent_is_file(self):
        self.make_file('parent')

        with self.assertRaises(CannotCreateDirParentNotADirectoryException):
            CreateDirectoryAction(self.full_test_path('parent/new_dir')).execute()

    def test_fail_parent_permissions(self):
        self.realize_file_structure('', (('DIR', 'parent', {'write': False}),))

        with self.assertRaises(CannotCreateDirNoPermissionsException):
            CreateDirectoryAction(self.full_test_path('parent/new_dir')).execute()

    def test_undo(self):
        path = self.full_test_path('test_dir')
        action = CreateDirectoryAction(path)

        action.execute()
        self.assert_is_dir(path)

        self.assertTrue(action.undo(), 'action.undo() failed unexpectedly')
        self.assert_path_does_not_exist(path)

    def test_fail_undo(self):
        action = CreateDirectoryAction(self.full_test_path('test_dir'))
        self.assertFalse(action.undo(), 'action.undo() succeeded unexpectedly')
