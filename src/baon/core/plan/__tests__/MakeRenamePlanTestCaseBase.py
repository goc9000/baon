# baon/core/plan/__tests__/MakeRenamePlanTestCaseBase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.__tests__.FileSystemTestCase import FileSystemTestCase
from baon.core.files.scan_files import scan_files
from baon.core.renaming.rename_files import rename_files

from baon.core.rules.RuleSet import RuleSet

from baon.core.plan.__errors__.make_rename_plan_errors import MakeRenamePlanError

from baon.core.plan.make_rename_plan import make_rename_plan

from baon.core.utils.lang_utils import is_arrayish, is_dictish, is_string
from baon.core.utils.str_utils import remove_prefix


class MakeRenamePlanTestCaseBase(FileSystemTestCase):

    def _test_make_rename_plan(self, files_repr, rules_text, expected_result, filter_scanned_files=None):
        base_path = self.resolve_test_path('')

        with self.temp_file_structure('', files_repr):
            files = scan_files(base_path, recursive=True)
            if filter_scanned_files is not None:
                files = [file_ref for file_ref in files if filter_scanned_files(file_ref)]

            rule_set = RuleSet.from_source(rules_text)
            renamed_files = rename_files(files, rule_set, use_path=False, use_extension=False)

            try:
                plan = make_rename_plan(base_path, renamed_files)
                result = plan.test_repr()
            except MakeRenamePlanError as e:
                result = e.test_repr()

            result = _relativize_result_paths(result, base_path)

            self.assertEquals(
                result,
                expected_result,
            )


def _relativize_result_paths(result, base_path):

    def recurse(item):
        if is_string(item):
            return remove_prefix(item, base_path)
        elif is_arrayish(item):
            return tuple(recurse(subitem) for subitem in item)
        elif is_dictish(item):
            return {key: recurse(value) for key, value in item.items()}
        else:
            return item

    return recurse(result)
