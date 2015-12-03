# baon/core/plan/__tests__/MakeRenamePlanTestCaseBase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.__tests__.FileSystemTestCase import FileSystemTestCase
from baon.core.plan.__errors__.make_rename_plan_errors import MakeRenamePlanError
from baon.core.plan.make_rename_plan import make_rename_plan
from baon.core.renaming.RenamedFileReference import RenamedFileReference
from baon.core.utils.lang_utils import is_arrayish, is_dictish, is_string
from baon.core.utils.str_utils import remove_prefix


class MakeRenamePlanTestCaseBase(FileSystemTestCase):

    def _test_make_rename_plan(self, renamed_files_repr, expected_result, actual_files=None, base_path_override=None):
        base_path = self.resolve_test_path('' if base_path_override is None else base_path_override)
        test_root = self.resolve_test_path('')

        renamed_files = [RenamedFileReference.from_test_repr(file_repr, base_path) for file_repr in renamed_files_repr]

        if actual_files is None:
            actual_files_repr = [file_ref.old_file_ref.test_repr() for file_ref in renamed_files]
        else:
            actual_files_repr = actual_files

        with self.temp_file_structure('', actual_files_repr):
            try:
                plan = make_rename_plan(renamed_files)
                result = plan.test_repr()
            except MakeRenamePlanError as e:
                result = e.test_repr()

            result = _relativize_result_paths(result, test_root)

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
