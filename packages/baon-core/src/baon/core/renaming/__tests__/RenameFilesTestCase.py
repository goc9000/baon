# baon/core/renaming/__tests__/RenameFilesTestCase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.files.FileReference import FileReference
from baon.core.renaming.rename_files import rename_files, apply_rename_overrides
from baon.core.rules.RuleSet import RuleSet
from baon.core.utils.baon_utils import convert_raw_overrides
from baon.core.utils.progress.ReportsProgressTestCase import ReportsProgressTestCase


class RenameFilesTestCase(ReportsProgressTestCase):

    def _test_rename_files(self, input_description, rules_text, expected_result, **options):
        files = [FileReference.from_test_repr(file_repr) for file_repr in input_description]
        rule_set = RuleSet.from_source(rules_text)

        rename_params = {key: value for key, value in options.items() if key != 'overrides'}
        renamed_files = rename_files(files, rule_set, **rename_params)

        if 'overrides' in options:
            # Normalize override specification
            overrides = {
                from_path.replace('/', os.sep): to_path.replace('/', os.sep)
                for from_path, to_path in options['overrides'].items()
            }

            renamed_files = apply_rename_overrides(renamed_files, convert_raw_overrides(overrides, None))

        self.assertEquals(
            tuple(f.test_repr() for f in renamed_files),
            expected_result,
        )
