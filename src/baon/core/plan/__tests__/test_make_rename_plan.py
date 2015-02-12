# baon/core/plan/__tests__/test_make_rename_plan.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.__tests__.FileSystemTestCase import FileSystemTestCase
from baon.core.parsing.parse_rules import parse_rules
from baon.core.files.scan_files import scan_files
from baon.core.renaming.rename_files import rename_files

from baon.core.plan.__errors__.make_rename_plan_errors import MakeRenamePlanError

from baon.core.plan.make_rename_plan import make_rename_plan


class TestMakeRenamePlan(FileSystemTestCase):

    def test_basic(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'dir1/file11.txt'),
                ('FILE', 'dir1/file12'),
                ('FILE', 'dir2/dir21/file211'),
                ('FILE', 'dir2/file21'),
                ('FILE', 'file1'),
                ('FILE', 'file2.bin'),
            ),
            '"file" "1"->"4"; "file42"->"dir3/file42"',
            (
                ('CreateDirectory', 'dir1/dir3'),
                ('MoveFile', 'dir1/file12', 'dir1/dir3/file42'),
                ('MoveFile', 'dir1/file11.txt', 'dir1/file41.txt'),
                ('MoveFile', 'file1', 'file4'),
                ('DeleteDirectoryIfEmpty', 'dir2/dir21'),
                ('DeleteDirectoryIfEmpty', 'dir2'),
                ('DeleteDirectoryIfEmpty', 'dir1'),
            ))

    def test_file_in_way_will_move(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file1'),
                ('FILE', 'file2'),
                ('FILE', 'entry'),
            ),
            '"entry"->"moved"; "file2"->"entry/file"',
            (
                ('MoveFile', 'entry', 'entry_1'),
                ('CreateDirectory', 'entry'),
                ('MoveFile', 'file2', 'entry/file'),
                ('MoveFile', 'entry_1', 'moved'),
            ))

    def test_file_in_way_will_not_move(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file1'),
                ('FILE', 'file2'),
                ('FILE', 'entry'),
            ),
            '"file2"->"entry/file"',
            ('CannotCreateDestinationDirFileInTheWayWillNotMoveError', {'destination_dir': 'entry'}))

    def test_file_in_way_will_move_find_free_name(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file1'),
                ('FILE', 'file2'),
                ('FILE', 'entry'),
            ),
            '"file1"->"entry_1"; "entry"->"moved" $; "file2"->"entry/file"',
            (
                ('MoveFile', 'entry', 'entry_2'),
                ('CreateDirectory', 'entry'),
                ('MoveFile', 'file2', 'entry/file'),
                ('MoveFile', 'file1', 'entry_1'),
                ('MoveFile', 'entry_2', 'moved'),
            ))

    def test_chain(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file1'),
                ('FILE', 'file2'),
                ('FILE', 'file3'),
                ('FILE', 'file4'),
            ),
            _make_permutation_rules([2, 3, 4, 5]),
            (
                ('MoveFile', 'file4', 'file5'),
                ('MoveFile', 'file3', 'file4'),
                ('MoveFile', 'file2', 'file3'),
                ('MoveFile', 'file1', 'file2'),
            ))

    def test_circular(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file1'),
                ('FILE', 'file2'),
                ('FILE', 'file3'),
                ('FILE', 'file4'),
            ),
            _make_permutation_rules([2, 3, 4, 1]),
            (
                ('MoveFile', 'file1', 'file1_1'),
                ('MoveFile', 'file4', 'file1'),
                ('MoveFile', 'file3', 'file4'),
                ('MoveFile', 'file2', 'file3'),
                ('MoveFile', 'file1_1', 'file2')
            ))

    def test_complex_permutation(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file1'),
                ('FILE', 'file2'),
                ('FILE', 'file3'),
                ('FILE', 'file4'),
                ('FILE', 'file5'),
                ('FILE', 'file6'),
                ('FILE', 'file7'),
                ('FILE', 'file8'),
            ),
            _make_permutation_rules([2, 10, 4, 5, 3, 7, 8, 9]),
            (
                ('MoveFile', 'file2', 'file10'),
                ('MoveFile', 'file1', 'file2'),
                ('MoveFile', 'file8', 'file9'),
                ('MoveFile', 'file7', 'file8'),
                ('MoveFile', 'file6', 'file7'),
                ('MoveFile', 'file3', 'file3_1'),
                ('MoveFile', 'file5', 'file3'),
                ('MoveFile', 'file4', 'file5'),
                ('MoveFile', 'file3_1', 'file4')
            ))

    def _test_make_rename_plan(self, files_repr, rules_text, expected_result):
        with self._temp_file_structure('', files_repr):
            files = scan_files(self._test_dir_path, recursive=True)
            rule_set = parse_rules(rules_text)
            renamed_files = rename_files(files, rule_set, use_path=False, use_extension=False)

            try:
                plan = make_rename_plan(self._test_dir_path, renamed_files)
                result = plan.test_repr()
            except MakeRenamePlanError as e:
                result = e.test_repr()

            self.assertEquals(
                result,
                expected_result,
            )


def _make_permutation_rules(permutation):
    return '"file" ({0})'.format('|'.join('"{0}"->"{1}"'.format(i+1, p_i) for i, p_i in enumerate(permutation)))
