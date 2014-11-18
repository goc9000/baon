# baon/core/renaming/__tests__/test_rename_files.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.__tests__.ReportsProgressTestCase import ReportsProgressTestCase

from baon.core.files.FileReference import FileReference

from baon.core.renaming.rename_files import rename_files
from baon.core.parsing.parse_rules import parse_rules


class TestRenameFiles(ReportsProgressTestCase):

    def test_basic(self):
        self._test_rename_files(
            input_description=(
                ('DIR', u'dir1'),
                ('DIR', u'dir2'),
                ('FILE', u'file1'),
                ('FILE', u'file2'),
                ('FILE', u'file3'),
            ),
            rules_text=u'..->paras',
            expected_result=(
                ('DIR', u'(dir1)'),
                ('DIR', u'(dir2)'),
                ('FILE', u'(file1)'),
                ('FILE', u'(file2)'),
                ('FILE', u'(file3)'),
            ),
        )

    def test_no_use_extension(self):
        self._test_rename_files(
            input_description=(
                ('DIR', u'dir1'),
                ('DIR', u'dir2.d'),
                ('FILE', u'file1.txt'),
                ('FILE', u'file2.txt'),
                ('FILE', u'file3'),
            ),
            rules_text=u'..->paras',
            expected_result=(
                ('DIR', u'(dir1)'),
                ('DIR', u'(dir2).d'),
                ('FILE', u'(file1).txt'),
                ('FILE', u'(file2).txt'),
                ('FILE', u'(file3)'),
            ),
            use_extension=False,
        )

    def test_use_extension(self):
        self._test_rename_files(
            input_description=(
                ('DIR', u'dir1'),
                ('DIR', u'dir2.d'),
                ('FILE', u'file1.txt'),
                ('FILE', u'file2.txt'),
                ('FILE', u'file3'),
            ),
            rules_text=u'..->paras',
            expected_result=(
                ('DIR', u'(dir1)'),
                ('DIR', u'(dir2.d)'),
                ('FILE', u'(file1.txt)'),
                ('FILE', u'(file2.txt)'),
                ('FILE', u'(file3)'),
            ),
            use_extension=True,
        )

    def test_no_use_path(self):
        self._test_rename_files(
            input_description=(
                ('FILE', u'dir1/file11.txt'),
                ('FILE', u'dir2.d/dir21/file211'),
                ('FILE', u'file1.txt'),
                ('FILE', u'file2.txt'),
                ('FILE', u'file3'),
            ),
            rules_text=u'..->paras',
            expected_result=(
                ('FILE', u'dir1/(file11).txt'),
                ('FILE', u'dir2.d/dir21/(file211)'),
                ('FILE', u'(file1).txt'),
                ('FILE', u'(file2).txt'),
                ('FILE', u'(file3)'),
            ),
            use_path=False,
        )

    def test_use_path(self):
        self._test_rename_files(
            input_description=(
                ('FILE', u'dir1/file11.txt'),
                ('FILE', u'dir2.d/dir21/file211'),
                ('FILE', u'file1.txt'),
                ('FILE', u'file2.txt'),
                ('FILE', u'file3'),
            ),
            rules_text=u'..->paras',
            expected_result=(
                ('FILE', u'(dir1/file11).txt'),
                ('FILE', u'(dir2.d/dir21/file211)'),
                ('FILE', u'(file1).txt'),
                ('FILE', u'(file2).txt'),
                ('FILE', u'(file3)'),
            ),
            use_path=True,
        )

    def test_error_unprintable_char_in_filename(self):
        self._test_rename_files(
            input_description=(('FILE', u'dir1/dir2/file.txt'),),
            rules_text=u'@"2"->"\\u0000"',
            expected_result=(('FILE', u'dir1/dir\u0000/file.txt', ('UnprintableCharacterInFilenameException',)),),
            use_path=True,
        )

    def test_error_empty_filename(self):
        self._test_rename_files(
            input_description=(('FILE', u'dir1/dir2/file.txt'),),
            rules_text=u'@"file.txt"!',
            expected_result=(('FILE', u'dir1/dir2/', ('EmptyFilenameException',)),),
            use_extension=True,
            use_path=True,
        )

    def test_error_only_dots_filename(self):
        self._test_rename_files(
            input_description=(('FILE', u'dir1/dir2/file.txt'),),
            rules_text=u'@"file.txt"->"."',
            expected_result=(('FILE', u'dir1/dir2/.', ('OnlyDotsFilenameException',)),),
            use_extension=True,
            use_path=True,
        )

    def test_error_empty_path_component(self):
        self._test_rename_files(
            input_description=(('FILE', u'dir1/dir2/file.txt'),),
            rules_text=u'@"dir2"!',
            expected_result=(('FILE', u'dir1//file.txt', ('EmptyPathComponentException',)),),
            use_path=True,
        )

    def test_error_multiple_empty_path_components(self):
        self._test_rename_files(
            input_description=(('FILE', u'dir1/dir2/file.txt'),),
            rules_text=u'@("dir" %d)!',
            # Note: only one exception is generated
            expected_result=(('FILE', u'//file.txt', ('EmptyPathComponentException',)),),
            use_path=True,
        )

    def test_error_only_dots_path_component(self):
        self._test_rename_files(
            input_description=(('FILE', u'dir1/dir2/file.txt'),),
            rules_text=u'@"dir2"->"."',
            expected_result=(('FILE', u'dir1/./file.txt', ('OnlyDotsPathComponentException',)),),
            use_path=True,
        )

    def test_error_multiple_only_dots_path_components(self):
        self._test_rename_files(
            input_description=(('FILE', u'dir1/dir2/file.txt'),),
            rules_text=u'@("dir" %d)->"."',
            # Note: only one exception is generated
            expected_result=(('FILE', u'././file.txt', ('OnlyDotsPathComponentException',)),),
            use_path=True,
        )

    def test_error_collision_file_vs_file(self):
        self._test_rename_files(
            input_description=(
                ('FILE', u'dir1/dir2/file1'),
                ('FILE', u'dir1/dir2/file2.txt'),
                ('FILE', u'dir1/dir2/file3.txt'),
            ),
            rules_text=u'@"2"->"3"',
            expected_result=(
                ('FILE', u'dir1/dir2/file1'),
                ('FILE', u'dir1/dir2/file3.txt', ('FileCollidesWithFileException',)),
                ('FILE', u'dir1/dir2/file3.txt', ('FileCollidesWithFileException',)),
            ),
        )

    def test_error_collision_dir_vs_file_direct(self):
        self._test_rename_files(
            input_description=(
                ('DIR', u'dir3'),
                ('FILE', u'file2.txt'),
                ('FILE', u'file3.txt'),
            ),
            rules_text=u'@"file3.txt"->"dir3"',
            expected_result=(
                ('DIR', u'dir3', ('DirectoryCollidesWithFileException',)),
                ('FILE', u'file2.txt'),
                ('FILE', u'dir3', ('FileCollidesWithDirectoryException',)),
            ),
            use_extension=True,
        )

    def test_error_collision_dir_vs_file_indirect(self):
        self._test_rename_files(
            input_description=(
                ('DIR', u'dir1/dir2/dir3'),
                ('FILE', u'dir1/dir2/file2.txt'),
                ('FILE', u'dir1/dir2/file3.txt'),
            ),
            rules_text=u'@"dir2/file3.txt"->"dir2"',
            expected_result=(
                ('DIR', u'dir1/dir2/dir3'),
                ('FILE', u'dir1/dir2/file2.txt'),
                ('FILE', u'dir1/dir2', ('FileCollidesWithDirectoryException',)),
            ),
            use_path=True,
            use_extension=True,
        )

    def test_error_collision_dir_vs_dir_direct(self):
        self._test_rename_files(
            input_description=(
                ('DIR', u'dir2'),
                ('DIR', u'dir3'),
                ('FILE', u'file1.txt'),
            ),
            rules_text=u'@"3"->"2"',
            expected_result=(
                ('DIR', u'dir2', ('WouldMergeImplicitlyWithOtherFoldersException',)),
                ('DIR', u'dir2', ('WouldMergeImplicitlyWithOtherFoldersException',)),
                ('FILE', u'file1.txt'),
            ),
        )

    def test_error_collision_dir_vs_dir_indirect(self):
        self._test_rename_files(
            input_description=(
                ('DIR', u'dir1/dir2/dir3'),
                ('FILE', u'dir1/dir2/file2.txt'),
                ('FILE', u'dir1/dir2/file3.txt'),
            ),
            rules_text=u'@"dir1/dir2/dir3"->"dir1"',
            expected_result=(
                ('DIR', u'dir1', ('WouldMergeImplicitlyWithOtherFoldersException',)),
                ('FILE', u'dir1/dir2/file2.txt'),
                ('FILE', u'dir1/dir2/file3.txt'),
            ),
            use_path=True,
            use_extension=True,
        )

    def test_warning_problematic_char_in_filename(self):
        self._test_rename_files(
            input_description=(('FILE', u'dir1/dir2/file.txt'),),
            rules_text=u'@"2"->"?"',
            expected_result=(('FILE', u'dir1/dir?/file.txt', ('ProblematicCharacterInFilenameWarning',)),),
            use_path=True,
        )

    def test_warning_space_before_component(self):
        self._test_rename_files(
            input_description=(('FILE', u'dir1/dir2/file.txt'),),
            rules_text=u'@(<<" " "dir2")',
            expected_result=(('FILE', u'dir1/ dir2/file.txt', ('PathComponentStartsWithSpaceWarning',)),),
            use_path=True,
        )

    def test_warning_space_after_component(self):
        self._test_rename_files(
            input_description=(('FILE', u'dir1/dir2/file.txt'),),
            rules_text=u'@("dir2" <<" ")',
            expected_result=(('FILE', u'dir1/dir2 /file.txt', ('PathComponentEndsWithSpaceWarning',)),),
            use_path=True,
        )

    def test_warning_double_spaces_in_component(self):
        self._test_rename_files(
            input_description=(
                ('FILE', u'dir1/dir2/file.txt'),
                ('FILE', u'dir1/dir3/file.txt'),
            ),
            rules_text=u'@"dir2"->"di r2";@"dir3"->"di  r3"',
            expected_result=(
                ('FILE', u'dir1/di r2/file.txt'),
                ('FILE', u'dir1/di  r3/file.txt', ('PathComponentContainsDoubleSpacesWarning',)),
            ),
            use_path=True,
        )

    def test_warning_space_before_filename(self):
        self._test_rename_files(
            input_description=(('FILE', u'dir1/dir2/file.txt'),),
            rules_text=u'@(<<" " "file")',
            expected_result=(('FILE', u'dir1/dir2/ file.txt', ('FilenameStartsWithSpaceWarning',)),),
        )

    def test_warning_space_after_filename(self):
        self._test_rename_files(
            input_description=(('FILE', u'dir1/dir2/file.txt'),),
            rules_text=u'@("file" <<" ")',
            expected_result=(('FILE', u'dir1/dir2/file .txt', ('BasenameEndsWithSpaceWarning',)),),
        )

    def test_warning_double_spaces_in_filename(self):
        self._test_rename_files(
            input_description=(
                ('FILE', u'dir1/dir2/file1.txt'),
                ('FILE', u'dir1/dir2/file2.txt'),
            ),
            rules_text=u'@"file1"->"fi le1";@"file2"->"fi  le2"',
            expected_result=(
                ('FILE', u'dir1/dir2/fi le1.txt'),
                ('FILE', u'dir1/dir2/fi  le2.txt', ('FilenameContainsDoubleSpacesWarning',)),
            ),
        )

    def test_warning_spaces_in_extension(self):
        self._test_rename_files(
            input_description=(
                ('FILE', u'dir1/dir2/file1'),
                ('FILE', u'dir1/dir2/file2.txt'),
                ('FILE', u'dir1/dir2/file3.txt'),
            ),
            rules_text=u'@"file1"->"fi le1";@"file2.txt"->"file2. txt";"file3.txt"->"file3.tx t"',
            expected_result=(
                ('FILE', u'dir1/dir2/fi le1'),
                ('FILE', u'dir1/dir2/file2. txt', ('ExtensionContainsSpacesWarning',)),
                ('FILE', u'dir1/dir2/file3.tx t', ('ExtensionContainsSpacesWarning',)),
            ),
            use_extension=True,
        )

    def test_reports_progress(self):
        progress_events = []

        self._test_rename_files(
            input_description=(('FILE', u'file{0}.txt'.format(i)) for i in xrange(10)),
            rules_text=u'"file" <<"0"',
            expected_result=tuple(('FILE', u'file0{0}.txt'.format(i)) for i in xrange(10)),
            on_progress=self._progress_collector(progress_events),
        )

        self._verify_reported_progress(progress_events)

    def _test_rename_files(self, input_description, rules_text, expected_result, **options):
        files = [
            FileReference(
                os.path.join(u'/', u'base', u'path', path),
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
