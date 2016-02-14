# baon/core/plan/actions/__tests__/test_CreateDirectoryAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.__tests__.FileSystemTestCase import requires_permissions_support
from baon.core.plan.actions.CreateDirectoryAction import CreateDirectoryAction
from baon.core.plan.actions.__errors__.plan_action_errors import CannotCreateDirAlreadyExistsError, \
    CannotCreateDirFileInWayError, CannotCreateDirParentDoesNotExistError, CannotCreateDirParentNotADirectoryError,\
    CannotCreateDirNoPermissionsError
from baon.core.plan.actions.__tests__.RenamePlanActionTestCase import RenamePlanActionTestCase


class TestCreateDirectoryAction(RenamePlanActionTestCase):

    def test_basic(self):
        self._make_action('created_dir').execute()

        self.assert_is_dir('created_dir')

    def test_fail_already_exists(self):
        self.make_dir('existing_dir')

        with self.assertRaises(CannotCreateDirAlreadyExistsError):
            self._make_action('existing_dir').execute()

    def test_fail_file_in_way(self):
        self.make_file('existing_file')

        with self.assertRaises(CannotCreateDirFileInWayError):
            self._make_action('existing_file').execute()

    def test_fail_no_parent(self):
        with self.assertRaises(CannotCreateDirParentDoesNotExistError):
            self._make_action('parent/new_dir').execute()

    def test_fail_parent_is_file(self):
        self.make_file('parent')

        with self.assertRaises(CannotCreateDirParentNotADirectoryError):
            self._make_action('parent/new_dir').execute()

    @requires_permissions_support
    def test_fail_parent_permissions(self):
        self.make_dir('parent', write=False)

        with self.assertRaises(CannotCreateDirNoPermissionsError):
            self._make_action('parent/new_dir').execute()

    def test_undo(self):
        action = self._make_action('test_dir')

        action.execute()
        self.assert_is_dir('test_dir')

        self.assertTrue(action.undo(), 'action.undo() failed unexpectedly')
        self.assert_path_does_not_exist('test_dir')

    def test_fail_undo(self):
        action = self._make_action('test_dir')
        self.assertFalse(action.undo(), 'action.undo() succeeded unexpectedly')

    def _make_action(self, path):
        return CreateDirectoryAction(self.resolve_test_path(path))
