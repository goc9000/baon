# baon/core/plan/__tests__/test_make_rename_plan_new.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.plan.__tests__.MakeRenamePlanNewTestCaseBase import MakeRenamePlanNewTestCaseBase


class TestMakeRenamePlan(MakeRenamePlanNewTestCaseBase):

    def test_empty_plan_if_no_files(self):
        self._test_make_rename_plan(
            (),
            (),
        )

    def test_empty_plan_if_no_changes(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'unchanged'),
            ),
            (),
        )
