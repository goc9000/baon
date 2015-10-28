# baon/core/renaming/__tests__/test_rename_warnings.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.renaming.__tests__.RenameFilesTestCase import RenameFilesTestCase


class TestRenameWarnings(RenameFilesTestCase):

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
            expected_result=(('FILE', 'dir1/dir2/file .txt', ('FilenameEndsWithSpaceWarning',)),),
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
                ('FILE', 'dir1/dir2/file4.txt'),
            ),
            rules_text='@"file1"->"fi le1";@"2.txt"->"2. txt";@"3.txt"->"3.tx t";@"4.txt"->"4.txt "',
            expected_result=(
                ('FILE', 'dir1/dir2/fi le1'),
                ('FILE', 'dir1/dir2/file2. txt', ('ExtensionContainsSpacesWarning',)),
                ('FILE', 'dir1/dir2/file3.tx t', ('ExtensionContainsSpacesWarning',)),
                ('FILE', 'dir1/dir2/file4.txt ', ('ExtensionContainsSpacesWarning',)),
            ),
            use_extension=True,
        )

    def test_warning_spaces_in_extension_different_rules_for_dirs(self):
        self._test_rename_files(
            input_description=(
                ('DIR', 'dir1/dir2/dir1'),
                ('DIR', 'dir1/dir2/dir2.old'),
                ('DIR', 'dir1/dir2/dir3.old'),
                ('DIR', 'dir1/dir2/dir4.old'),
            ),
            rules_text='"dir1"->"new dir";"dir2.old"->"01. title";"dir3.old"->"02.b. a b";"dir4.old"->"03. dir "',
            expected_result=(
                ('DIR', 'dir1/dir2/new dir'),
                ('DIR', 'dir1/dir2/01. title'),
                ('DIR', 'dir1/dir2/02.b. a b'),
                ('DIR', 'dir1/dir2/03. dir ', ('FilenameEndsWithSpaceWarning',)),
            ),
            use_extension=True,
        )

    def test_warning_in_input_is_ignored(self):
        self._test_rename_files(
            input_description=(
                ('FILE', 'file1'),
                ('FILE', 'file2', ('SyntheticFileWarning',)),
                ('FILE', 'file3'),
            ),
            rules_text="'file' <<'0'",
            expected_result=(
                ('FILE', 'file01'),
                ('FILE', 'file02'),
                ('FILE', 'file03'),
            ),
        )
