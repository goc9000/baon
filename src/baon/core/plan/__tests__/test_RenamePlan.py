# baon/core/plan/__tests__/test_RenamePlan.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.plan.RenamePlan import RenamePlan
from baon.core.plan.__tests__.RenamePlanTestCaseBase import RenamePlanTestCaseBase


class TestRenamePlan(RenamePlanTestCaseBase):

    def test_parse_basic(self):
        reconstructed_plan = RenamePlan.from_json_representation(self.RENAME_PLAN_EXAMPLE.json_representation())

        self.assertEqual(
            reconstructed_plan.test_repr(),
            (
                ('CreateDirectory', '/base/dest_dir'),
                ('MoveFile', '/base/src_dir/file1', '/base/dest_dir/file2'),
                ('DeleteDirectoryIfEmpty', '/base/src_dir'),
            )
        )

    def test_parse_empty(self):
        reconstructed_plan = RenamePlan.from_json_representation({
            'steps': [],
        })
        self.assertEqual(reconstructed_plan.test_repr(), ())

    def test_parse_malformed(self):
        for json_repr in (
            123,
            'bogus',
            (1, 2, 3),
            {},
            {'steps': (1, 2, 3)},
            {'steps': (('InvalidAction', 'path'),)},
            {'steps': (('CreateDirectory', 'path', 'path2'),)},
        ):
            with self.subTest(json_repr=json_repr):
                with self.assertRaises(ValueError):
                    RenamePlan.from_json_representation(json_repr)
