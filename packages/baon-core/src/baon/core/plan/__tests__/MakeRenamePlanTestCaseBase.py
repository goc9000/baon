# baon/core/plan/__tests__/MakeRenamePlanTestCaseBase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.__tests__.FileSystemTestCase import FileSystemTestCase
from baon.core.plan.__errors__.make_rename_plan_errors import MakeRenamePlanError
from baon.core.plan.make_rename_plan import make_rename_plan, staging_dir_variants
from baon.core.renaming.RenamedFileReference import RenamedFileReference
from baon.core.utils.lang_utils import is_arrayish, is_dictish, is_string
from baon.core.utils.str_utils import remove_prefix


class MakeRenamePlanTestCaseBase(FileSystemTestCase):

    def _test_make_rename_plan(
        self,
        renamed_files_repr,
        expected_result,
        actual_files=None,
        base_path_override=None,
        case_insensitive_override=None,
    ):
        base_path = self.resolve_test_path('' if base_path_override is None else base_path_override)
        test_root = self.resolve_test_path('')

        renamed_files = [
            RenamedFileReference.from_test_repr(file_repr, base_path)
            for file_repr in _normalize_input_files(renamed_files_repr)
        ]

        if actual_files is None:
            actual_files_repr = [file_ref.old_file_ref.test_repr() for file_ref in renamed_files]
        else:
            actual_files_repr = _normalize_input_files(actual_files)

        with self.temp_file_structure('', actual_files_repr):
            try:
                plan = make_rename_plan(renamed_files, case_insensitive_filesystem=case_insensitive_override)
                result = plan.test_repr()
            except MakeRenamePlanError as e:
                result = e.test_repr()

            self.assertEquals(
                _normalize_actual_result(result, test_root),
                _normalize_expected_result(expected_result),
            )


dir_variants = staging_dir_variants()
base_staging_dir = next(dir_variants)
alt_staging_dir = next(dir_variants)


def _replace_recursive(structure, *scalar_replace_functions):
    def _replace_scalar(value):
        for replace_function in scalar_replace_functions:
            value = replace_function(value)
        return value

    def _replace_rec(value):
        if is_string(value):
            return _replace_scalar(value)
        elif is_arrayish(value):
            return tuple(_replace_rec(subitem) for subitem in value)
        elif is_dictish(value):
            return {key: _replace_rec(value) for key, value in value.items()}
        else:
            return value

    return _replace_rec(structure)


def _replace_staging_dir_placeholders(path_text):
    return path_text.replace('<STAGING_DIR>', base_staging_dir).replace('<ALTERNATE_STAGING_DIR>', alt_staging_dir)


def _normalize_input_files(files_repr):
    return _replace_recursive(
        files_repr,
        _replace_staging_dir_placeholders,
    )


def _normalize_actual_result(result, base_path):
    """
    Normalizes the actual result by relativizing the absolute paths such that they can be compared with the
    necessarily relative paths in the expected result
    """
    return _replace_recursive(
        result,
        lambda item: remove_prefix(item, base_path),
    )


def _normalize_expected_result(expected_result):
    """
    Normalizes the expected result by replacing placeholders like <STAGING_DIR> with the actual directory name.
    """
    return _replace_recursive(
        expected_result,
        _replace_staging_dir_placeholders,
    )
