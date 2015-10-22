# baon/core/renaming/__tests__/RenameFilesTestCase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.utils.progress.ReportsProgressTestCase import ReportsProgressTestCase

from baon.core.files.FileReference import FileReference
from baon.core.files.__errors__.file_reference_errors import SyntheticFileError, \
    SyntheticFileWarning

from baon.core.renaming.rename_files import rename_files, apply_rename_overrides

from baon.core.parsing.parse_rules import parse_rules


class RenameFilesTestCase(ReportsProgressTestCase):

    def _test_rename_files(self, input_description, rules_text, expected_result, **options):
        files = [self._file_from_test_repr(file_repr) for file_repr in input_description]
        rule_set = parse_rules(rules_text)

        rename_params = {key: value for key, value in options.items() if key != 'overrides'}
        renamed_files = rename_files(files, rule_set, **rename_params)

        if 'overrides' in options:
            renamed_files = apply_rename_overrides(renamed_files, options['overrides'])

        self.assertEquals(
            tuple(f.test_repr() for f in renamed_files),
            expected_result,
        )

    @staticmethod
    def _file_from_test_repr(file_test_repr):
        assert len(file_test_repr) >= 2

        file_type, path = file_test_repr[:2]

        file_ref = FileReference(
            os.path.join('/', 'base', 'path', path),
            path,
            file_type == 'DIR',
        )

        if len(file_test_repr) >= 3:
            for error_repr in file_test_repr[2]:
                assert error_repr in ['SyntheticFileError', 'SyntheticFileWarning'],\
                    'Only SyntheticFileError and SyntheticFileWarning are supported'

                if error_repr == 'SyntheticFileError':
                    file_ref.problems.append(SyntheticFileError())
                elif error_repr == 'SyntheticFileWarning':
                    file_ref.problems.append(SyntheticFileWarning())

        return file_ref
