# baon/core/plan/__tests__/test_RenamePlan_load_save.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.__tests__.FileSystemTestCase import FileSystemTestCase

from baon.core.plan.__errors__.rename_plan_errors import CannotSaveRenamePlanFailedWritingFileError,\
    CannotSaveRenamePlanPermissionsError, CannotLoadRenamePlanFailedReadingFileError, \
    CannotLoadRenamePlanInvalidFormatError, CannotLoadRenamePlanPermissionsError

from baon.core.plan.__tests__.RenamePlanTestCaseBase import RenamePlanTestCaseBase

from baon.core.plan.RenamePlan import RenamePlan


class TestRenamePlanLoadSave(RenamePlanTestCaseBase, FileSystemTestCase):

    def test_save_plan(self):
        self._test_save_plan('saved_plan.json')

        self.assert_is_file('saved_plan.json')

    def test_save_plan_overwrite(self):
        self.make_file('plan.json', contents='OVERWRITE_ME')

        self._test_save_plan('plan.json')

        self.assert_file_contents_not('plan.json', 'OVERWRITE_ME')

    def test_save_plan_fail_write(self):
        self.make_file('not_a_dir')

        with self.assertRaises(CannotSaveRenamePlanFailedWritingFileError):
            self._test_save_plan('not_a_dir/plan.json')

    def test_save_plan_fail_permissions(self):
        self.make_dir('no_write_dir', write=False)

        with self.assertRaises(CannotSaveRenamePlanPermissionsError):
            self._test_save_plan('no_write_dir/plan.json')

    def _test_save_plan(self, path):
        self.RENAME_PLAN_EXAMPLE.save_to_file(self.resolve_test_path(path))

    def test_save_reload(self):
        self._test_save_plan('plan.json')

        self.assertEqual(self.RENAME_PLAN_EXAMPLE, self._test_load_plan('plan.json'))

    def test_save_reload_unicode(self):
        self.UNICODE_RENAME_PLAN_EXAMPLE.save_to_file(self.resolve_test_path('unicode_plan.json'))

        self.assertEqual(self.UNICODE_RENAME_PLAN_EXAMPLE, self._test_load_plan('unicode_plan.json'))

    def test_load_fail_missing(self):
        with self.assertRaises(CannotLoadRenamePlanFailedReadingFileError):
            self._test_load_plan('missing_file.json')

    def test_load_fail_permissions(self):
        self.make_file('locked.json', read=False)

        with self.assertRaises(CannotLoadRenamePlanPermissionsError):
            self._test_load_plan('locked.json')

    def test_load_fail_corrupt_not_json(self):
        self._test_save_plan('original.json')
        contents = self.get_file_contents('original.json')
        self.make_file('corrupt.json', contents=contents[:len(contents) // 2])

        with self.assertRaises(CannotLoadRenamePlanInvalidFormatError):
            self._test_load_plan('corrupt.json')

    def test_load_fail_corrupt_json_but_invalid(self):
        self.make_file('corrupt.json', contents='[["BogusAction", "path"]]')

        with self.assertRaises(CannotLoadRenamePlanInvalidFormatError):
            self._test_load_plan('corrupt.json')

    def _test_load_plan(self, path):
        return RenamePlan.load_from_file(self.resolve_test_path(path))
