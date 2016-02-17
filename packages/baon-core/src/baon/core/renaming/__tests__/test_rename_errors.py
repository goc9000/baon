# baon/core/renaming/__tests__/test_rename_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.renaming.__tests__.RenameFilesTestCase import RenameFilesTestCase


class TestRenameErrors(RenameFilesTestCase):

    def test_error_unprintable_char_in_filename(self):
        self._test_rename_files(
            input_description=(('FILE', 'dir1/dir2/file.txt'),),
            rules_text='@"2"->"\u0000"',
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
            rules_text='.. "dir2" (%c "file3.txt")!',
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
            rules_text='(%path "dir3")->"dir1"',
            expected_result=(
                ('DIR', 'dir1', ('WouldMergeImplicitlyWithOtherFoldersError',)),
                ('FILE', 'dir1/dir2/file2.txt'),
                ('FILE', 'dir1/dir2/file3.txt'),
            ),
            use_path=True,
            use_extension=True,
        )

    def test_error_in_input_causes_error_if_renamed(self):
        self._test_rename_files(
            input_description=(
                ('FILE', 'file1'),
                ('FILE', 'file2', ('SyntheticFileError',)),
                ('FILE', 'file3'),
            ),
            rules_text="'file' <<'0'",
            expected_result=(
                ('FILE', 'file01'),
                ('FILE', 'file02', ('CannotRenameFileWithErrorsError',)),
                ('FILE', 'file03'),
            ),
        )

    def test_error_in_input_is_ok_if_not_renamed(self):
        self._test_rename_files(
            input_description=(
                ('FILE', 'file1'),
                ('FILE', 'file2', ('SyntheticFileError',)),
                ('FILE', 'file3'),
            ),
            rules_text="'file' <<'0' ('1'|'3')",
            expected_result=(
                ('FILE', 'file01'),
                ('FILE', 'file2'),
                ('FILE', 'file03'),
            ),
        )
