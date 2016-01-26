# baon/core/plan/__tests__/test_rename_plan_backup.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest.mock import patch

from baon.core.__tests__.FileSystemTestCase import FileSystemTestCase
from baon.core.plan.__tests__.RenamePlanTestCaseBase import RenamePlanTestCaseBase
from baon.core.plan.rename_plan_backup import rename_plan_backup_exists, save_rename_plan_backup,\
    load_rename_plan_backup, delete_rename_plan_backup


class TestRenamePlanBackup(RenamePlanTestCaseBase, FileSystemTestCase):

    def test_basic(self):
        with patch(
            'baon.core.plan.rename_plan_backup.get_rename_plan_backup_filename',
            new=lambda: self.resolve_test_path('backup.json'),
        ):
            self.assertFalse(rename_plan_backup_exists())

            save_rename_plan_backup(self.RENAME_PLAN_EXAMPLE)

            self.assertTrue(rename_plan_backup_exists())

            reloaded_plan = load_rename_plan_backup()

            self.assertEqual(reloaded_plan, self.RENAME_PLAN_EXAMPLE)

            delete_rename_plan_backup()

            self.assertFalse(rename_plan_backup_exists())
