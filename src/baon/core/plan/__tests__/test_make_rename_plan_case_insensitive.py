# baon/core/plan/__tests__/test_make_rename_plan_case_insensitive.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.__tests__.FileSystemTestCase import requires_case_insensitive_filesystem
from baon.core.plan.__tests__.MakeRenamePlanTestCaseBase import MakeRenamePlanTestCaseBase


class TestMakeRenamePlanCaseInsensitive(MakeRenamePlanTestCaseBase):

    @requires_case_insensitive_filesystem
    def test_change_case(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file', 'FILE'),
            ),
            (
                ('CreateDirectory', '<STAGING_DIR>'),
                ('MoveFile', 'file', '<STAGING_DIR>/FILE'),
                ('MoveFile', '<STAGING_DIR>/FILE', 'FILE'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>'),
            ),
        )
