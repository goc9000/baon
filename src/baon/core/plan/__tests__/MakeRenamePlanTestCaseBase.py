# baon/core/plan/__tests__/MakeRenamePlanTestCaseBase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.__tests__.FileSystemTestCase import FileSystemTestCase
from baon.core.parsing.parse_rules import parse_rules
from baon.core.files.scan_files import scan_files
from baon.core.renaming.rename_files import rename_files

from baon.core.plan.__errors__.make_rename_plan_errors import MakeRenamePlanError

from baon.core.plan.make_rename_plan import make_rename_plan

from baon.core.utils.lang_utils import is_arrayish, is_string


class MakeRenamePlanTestCaseBase(FileSystemTestCase):

    def _test_make_rename_plan(self, files_repr, rules_text, expected_result, filter_scanned_files=None):
        base_path = self.resolve_test_path('')

        if len(expected_result) > 0 and is_arrayish(expected_result[0]):
            expected_result = _apply_base_path_to_expected_result(expected_result, base_path)

        with self.temp_file_structure('', files_repr):
            files = scan_files(base_path, recursive=True)
            if filter_scanned_files is not None:
                files = [file_ref for file_ref in files if filter_scanned_files(file_ref)]

            rule_set = parse_rules(rules_text)
            renamed_files = rename_files(files, rule_set, use_path=False, use_extension=False)

            try:
                plan = make_rename_plan(base_path, renamed_files)
                result = plan.test_repr()
            except MakeRenamePlanError as e:
                result = e.test_repr()

            self.assertEquals(
                result,
                expected_result,
            )


def _apply_base_path_to_expected_result(expected_result, base_path):
    return tuple(_apply_base_path_to_action_repr(action_repr, base_path) for action_repr in expected_result)


def _apply_base_path_to_action_repr(action_repr, base_path):
    return (action_repr[0],) + tuple(
        os.path.join(base_path, value) if is_string(value) else value for value in action_repr[1:]
    )
