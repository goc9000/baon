# baon/core/plan/__tests__/test_RenamePlan.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.core.plan.RenamePlan import RenamePlan
from baon.core.plan.actions.CreateDirectoryAction import CreateDirectoryAction
from baon.core.plan.actions.MoveFileAction import MoveFileAction
from baon.core.plan.actions.DeleteDirectoryIfEmptyAction import DeleteDirectoryIfEmptyAction


class TestRenamePlan(TestCase):

    RENAME_PLAN_EXAMPLE = RenamePlan([
        CreateDirectoryAction('/base/dest_dir'),
        MoveFileAction('/base/src_dir/file1', '/base/dest_dir/file2'),
        DeleteDirectoryIfEmptyAction('/base/src_dir'),
    ])

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
        reconstructed_plan = RenamePlan.from_json_representation([])
        self.assertEqual(reconstructed_plan.test_repr(), ())

    def test_parse_malformed(self):
        for json_repr in (
            123,
            'bogus',
            {},
            (1, 2, 3),
            (('InvalidAction', 'path'),),
            (('CreateDirectory', 'path', 'path2'),),
        ):
            with self.subTest(json_repr=json_repr):
                with self.assertRaises(ValueError):
                    RenamePlan.from_json_representation(json_repr)
