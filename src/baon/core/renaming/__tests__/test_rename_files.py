# baon/core/renaming/__tests__/test_rename_files.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.utils.progress.ReportsProgressTestCase import ReportsProgressTestCase

from baon.core.files.FileReference import FileReference

from baon.core.renaming.rename_files import rename_files
from baon.core.parsing.parse_rules import parse_rules


class TestRenameFiles(ReportsProgressTestCase):

    def test_basic(self):
        self._test_rename_files(
            input_description=(
                ('DIR', 'dir1'),
                ('DIR', 'dir2'),
                ('FILE', 'file1'),
                ('FILE', 'file2'),
                ('FILE', 'file3'),
            ),
            rules_text='..->paras',
            expected_result=(
                ('DIR', '(dir1)'),
                ('DIR', '(dir2)'),
                ('FILE', '(file1)'),
                ('FILE', '(file2)'),
                ('FILE', '(file3)'),
            ),
        )

    def test_no_use_extension(self):
        self._test_rename_files(
            input_description=(
                ('DIR', 'dir1'),
                ('DIR', 'dir2.d'),
                ('FILE', 'file1.txt'),
                ('FILE', 'file2.txt'),
                ('FILE', 'file3'),
            ),
            rules_text='..->paras',
            expected_result=(
                ('DIR', '(dir1)'),
                ('DIR', '(dir2).d'),
                ('FILE', '(file1).txt'),
                ('FILE', '(file2).txt'),
                ('FILE', '(file3)'),
            ),
            use_extension=False,
        )

    def test_use_extension(self):
        self._test_rename_files(
            input_description=(
                ('DIR', 'dir1'),
                ('DIR', 'dir2.d'),
                ('FILE', 'file1.txt'),
                ('FILE', 'file2.txt'),
                ('FILE', 'file3'),
            ),
            rules_text='..->paras',
            expected_result=(
                ('DIR', '(dir1)'),
                ('DIR', '(dir2.d)'),
                ('FILE', '(file1.txt)'),
                ('FILE', '(file2.txt)'),
                ('FILE', '(file3)'),
            ),
            use_extension=True,
        )

    def test_no_use_path(self):
        self._test_rename_files(
            input_description=(
                ('FILE', 'dir1/file11.txt'),
                ('FILE', 'dir2.d/dir21/file211'),
                ('FILE', 'file1.txt'),
                ('FILE', 'file2.txt'),
                ('FILE', 'file3'),
            ),
            rules_text='..->paras',
            expected_result=(
                ('FILE', 'dir1/(file11).txt'),
                ('FILE', 'dir2.d/dir21/(file211)'),
                ('FILE', '(file1).txt'),
                ('FILE', '(file2).txt'),
                ('FILE', '(file3)'),
            ),
            use_path=False,
        )

    def test_use_path(self):
        self._test_rename_files(
            input_description=(
                ('FILE', 'dir1/file11.txt'),
                ('FILE', 'dir2.d/dir21/file211'),
                ('FILE', 'file1.txt'),
                ('FILE', 'file2.txt'),
                ('FILE', 'file3'),
            ),
            rules_text='..->paras',
            expected_result=(
                ('FILE', '(dir1/file11).txt'),
                ('FILE', '(dir2.d/dir21/file211)'),
                ('FILE', '(file1).txt'),
                ('FILE', '(file2).txt'),
                ('FILE', '(file3)'),
            ),
            use_path=True,
        )

    def test_override(self):
        self._test_rename_files(
            input_description=(
                ('FILE', 'dir1/file11.txt'),
                ('FILE', 'dir2.d/dir21/file211'),
                ('FILE', 'file1.txt'),
                ('FILE', 'file2.txt'),
                ('FILE', 'file3'),
            ),
            rules_text='..->paras',
            expected_result=(
                ('FILE', 'dir3/dir4/[file341].bin', 'OVERRIDE'),
                ('FILE', 'dir2.d/dir21/(file211)'),
                ('FILE', 'file100.txt', 'OVERRIDE'),
                ('FILE', '(file2).txt'),
                ('FILE', '(file3)'),
            ),
            use_path=False,
            overrides={
                'file1.txt': 'file100.txt',
                'dir1/file11.txt': 'dir3/dir4/[file341].bin',
            },
        )

    def test_error_unprintable_char_in_filename(self):
        self._test_rename_files(
            input_description=(('FILE', 'dir1/dir2/file.txt'),),
            rules_text='@"2"->"\\u0000"',
            expected_result=(('FILE', 'dir1/dir\u0000/file.txt', ('UnprintableCharacterInFilenameError',)),),
            use_path=True,
        )

    def test_error_empty_filename(self):
        self._test_rename_files(
            input_description=(('FILE', 'dir1/dir2/file.txt'),),
            rules_text='@"file.txt"!',
            expected_result=(('FILE', 'dir1/dir2/', ('EmptyFilenameError',)),),
            use_extension=True,
            use_path=True,
        )

    def test_error_only_dots_filename(self):
        self._test_rename_files(
            input_description=(('FILE', 'dir1/dir2/file.txt'),),
            rules_text='@"file.txt"->"."',
            expected_result=(('FILE', 'dir1/dir2/.', ('OnlyDotsFilenameError',)),),
            use_extension=True,
            use_path=True,
        )

    def test_error_empty_path_component(self):
        self._test_rename_files(
            input_description=(('FILE', 'dir1/dir2/file.txt'),),
            rules_text='@"dir2"!',
            expected_result=(('FILE', 'dir1//file.txt', ('EmptyPathComponentError',)),),
            use_path=True,
        )

    def test_error_multiple_empty_path_components(self):
        self._test_rename_files(
            input_description=(('FILE', 'dir1/dir2/file.txt'),),
            rules_text='@("dir" %d)!',
            # Note: only one exception is generated
            expected_result=(('FILE', '//file.txt', ('EmptyPathComponentError',)),),
            use_path=True,
        )

    def test_error_only_dots_path_component(self):
        self._test_rename_files(
            input_description=(('FILE', 'dir1/dir2/file.txt'),),
            rules_text='@"dir2"->"."',
            expected_result=(('FILE', 'dir1/./file.txt', ('OnlyDotsPathComponentError',)),),
            use_path=True,
        )

    def test_error_multiple_only_dots_path_components(self):
        self._test_rename_files(
            input_description=(('FILE', 'dir1/dir2/file.txt'),),
            rules_text='@("dir" %d)->"."',
            # Note: only one exception is generated
            expected_result=(('FILE', '././file.txt', ('OnlyDotsPathComponentError',)),),
            use_path=True,
        )

    def test_error_collision_file_vs_file(self):
        self._test_rename_files(
            input_description=(
                ('FILE', 'dir1/dir2/file1'),
                ('FILE', 'dir1/dir2/file2.txt'),
                ('FILE', 'dir1/dir2/file3.txt'),
            ),
            rules_text='@"2"->"3"',
            expected_result=(
                ('FILE', 'dir1/dir2/file1'),
                ('FILE', 'dir1/dir2/file3.txt', ('FileCollidesWithFileError',)),
                ('FILE', 'dir1/dir2/file3.txt', ('FileCollidesWithFileError',)),
            ),
        )

    def test_error_collision_dir_vs_file_direct(self):
        self._test_rename_files(
            input_description=(
                ('DIR', 'dir3'),
                ('FILE', 'file2.txt'),
                ('FILE', 'file3.txt'),
            ),
            rules_text='@"file3.txt"->"dir3"',
            expected_result=(
                ('DIR', 'dir3', ('DirectoryCollidesWithFileError',)),
                ('FILE', 'file2.txt'),
                ('FILE', 'dir3', ('FileCollidesWithDirectoryError',)),
            ),
            use_extension=True,
        )

    def test_error_collision_dir_vs_file_indirect(self):
        self._test_rename_files(
            input_description=(
                ('DIR', 'dir1/dir2/dir3'),
                ('FILE', 'dir1/dir2/file2.txt'),
                ('FILE', 'dir1/dir2/file3.txt'),
            ),
            rules_text='@"dir2/file3.txt"->"dir2"',
            expected_result=(
                ('DIR', 'dir1/dir2/dir3'),
                ('FILE', 'dir1/dir2/file2.txt'),
                ('FILE', 'dir1/dir2', ('FileCollidesWithDirectoryError',)),
            ),
            use_path=True,
            use_extension=True,
        )

    def test_error_collision_dir_vs_dir_direct(self):
        self._test_rename_files(
            input_description=(
                ('DIR', 'dir2'),
                ('DIR', 'dir3'),
                ('FILE', 'file1.txt'),
            ),
            rules_text='@"3"->"2"',
            expected_result=(
                ('DIR', 'dir2', ('WouldMergeImplicitlyWithOtherFoldersError',)),
                ('DIR', 'dir2', ('WouldMergeImplicitlyWithOtherFoldersError',)),
                ('FILE', 'file1.txt'),
            ),
        )

    def test_error_collision_dir_vs_dir_indirect(self):
        self._test_rename_files(
            input_description=(
                ('DIR', 'dir1/dir2/dir3'),
                ('FILE', 'dir1/dir2/file2.txt'),
                ('FILE', 'dir1/dir2/file3.txt'),
            ),
            rules_text='@"dir1/dir2/dir3"->"dir1"',
            expected_result=(
                ('DIR', 'dir1', ('WouldMergeImplicitlyWithOtherFoldersError',)),
                ('FILE', 'dir1/dir2/file2.txt'),
                ('FILE', 'dir1/dir2/file3.txt'),
            ),
            use_path=True,
            use_extension=True,
        )

    def test_warning_problematic_char_in_filename(self):
        self._test_rename_files(
            input_description=(('FILE', 'dir1/dir2/file.txt'),),
            rules_text='@"2"->"?"',
            expected_result=(('FILE', 'dir1/dir?/file.txt', ('ProblematicCharacterInFilenameWarning',)),),
            use_path=True,
        )

    def test_warning_space_before_component(self):
        self._test_rename_files(
            input_description=(('FILE', 'dir1/dir2/file.txt'),),
            rules_text='@(<<" " "dir2")',
            expected_result=(('FILE', 'dir1/ dir2/file.txt', ('PathComponentStartsWithSpaceWarning',)),),
            use_path=True,
        )

    def test_warning_space_after_component(self):
        self._test_rename_files(
            input_description=(('FILE', 'dir1/dir2/file.txt'),),
            rules_text='@("dir2" <<" ")',
            expected_result=(('FILE', 'dir1/dir2 /file.txt', ('PathComponentEndsWithSpaceWarning',)),),
            use_path=True,
        )

    def test_warning_double_spaces_in_component(self):
        self._test_rename_files(
            input_description=(
                ('FILE', 'dir1/dir2/file.txt'),
                ('FILE', 'dir1/dir3/file.txt'),
            ),
            rules_text='@"dir2"->"di r2";@"dir3"->"di  r3"',
            expected_result=(
                ('FILE', 'dir1/di r2/file.txt'),
                ('FILE', 'dir1/di  r3/file.txt', ('PathComponentContainsDoubleSpacesWarning',)),
            ),
            use_path=True,
        )

    def test_warning_space_before_filename(self):
        self._test_rename_files(
            input_description=(('FILE', 'dir1/dir2/file.txt'),),
            rules_text='@(<<" " "file")',
            expected_result=(('FILE', 'dir1/dir2/ file.txt', ('FilenameStartsWithSpaceWarning',)),),
        )

    def test_warning_space_after_filename(self):
        self._test_rename_files(
            input_description=(('FILE', 'dir1/dir2/file.txt'),),
            rules_text='@("file" <<" ")',
            expected_result=(('FILE', 'dir1/dir2/file .txt', ('BasenameEndsWithSpaceWarning',)),),
        )

    def test_warning_double_spaces_in_filename(self):
        self._test_rename_files(
            input_description=(
                ('FILE', 'dir1/dir2/file1.txt'),
                ('FILE', 'dir1/dir2/file2.txt'),
            ),
            rules_text='@"file1"->"fi le1";@"file2"->"fi  le2"',
            expected_result=(
                ('FILE', 'dir1/dir2/fi le1.txt'),
                ('FILE', 'dir1/dir2/fi  le2.txt', ('FilenameContainsDoubleSpacesWarning',)),
            ),
        )

    def test_warning_spaces_in_extension(self):
        self._test_rename_files(
            input_description=(
                ('FILE', 'dir1/dir2/file1'),
                ('FILE', 'dir1/dir2/file2.txt'),
                ('FILE', 'dir1/dir2/file3.txt'),
            ),
            rules_text='@"file1"->"fi le1";@"file2.txt"->"file2. txt";"file3.txt"->"file3.tx t"',
            expected_result=(
                ('FILE', 'dir1/dir2/fi le1'),
                ('FILE', 'dir1/dir2/file2. txt', ('ExtensionContainsSpacesWarning',)),
                ('FILE', 'dir1/dir2/file3.tx t', ('ExtensionContainsSpacesWarning',)),
            ),
            use_extension=True,
        )

    def test_reports_progress(self):
        with self.verify_reported_progress() as on_progress:
            self._test_rename_files(
                input_description=(('FILE', 'file{0}.txt'.format(i)) for i in range(10)),
                rules_text='"file" <<"0"',
                expected_result=tuple(('FILE', 'file0{0}.txt'.format(i)) for i in range(10)),
                on_progress=on_progress,
            )

    def _test_rename_files(self, input_description, rules_text, expected_result, **options):
        files = [
            FileReference(
                os.path.join('/', 'base', 'path', path),
                path,
                file_type == 'DIR',
            )
            for file_type, path in input_description
        ]

        rule_set = parse_rules(rules_text)

        renamed_files = rename_files(files, rule_set, **options)

        self.assertEquals(
            tuple(f.test_repr() for f in renamed_files),
            expected_result,
        )
