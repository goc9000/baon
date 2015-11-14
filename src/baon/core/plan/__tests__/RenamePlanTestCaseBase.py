# baon/core/plan/__tests__/RenamePlanTestCaseBase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from unittest import TestCase

from baon.core.plan.RenamePlan import RenamePlan
from baon.core.plan.actions.CreateDirectoryAction import CreateDirectoryAction
from baon.core.plan.actions.DeleteDirectoryIfEmptyAction import DeleteDirectoryIfEmptyAction
from baon.core.plan.actions.MoveFileAction import MoveFileAction


class RenamePlanTestCaseBase(TestCase):

    RENAME_PLAN_EXAMPLE = RenamePlan([
        CreateDirectoryAction('/base/dest_dir'),
        MoveFileAction('/base/src_dir/file1', '/base/dest_dir/file2'),
        DeleteDirectoryIfEmptyAction('/base/src_dir'),
    ])

    UNICODE_RENAME_PLAN_EXAMPLE = RenamePlan([
        CreateDirectoryAction('/bas\u00e9/dest_dir'),
        MoveFileAction('/bas\u00e9/src_di\u0453/fil\u00e91', '/bas\u00e9/dest_dir/f\u0457le2'),
        DeleteDirectoryIfEmptyAction('/bas\u00e9/src_di\u0453'),
    ])
