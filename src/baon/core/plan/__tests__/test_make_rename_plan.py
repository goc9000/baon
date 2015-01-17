# baon/core/plan/__tests__/test_make_rename_plan.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.__tests__.FileSystemTestCase import FileSystemTestCase
from baon.core.parsing.parse_rules import parse_rules
from baon.core.files.scan_files import scan_files
from baon.core.renaming.rename_files import rename_files
from baon.core.plan.make_rename_plan import make_rename_plan
from baon.core.plan.make_rename_plan_exceptions import MakeRenamePlanException


class TestMakeRenamePlan(FileSystemTestCase):

    @classmethod
    def setup_test_files_basic(cls):
        cls._make_file('basic/dir1/file11.txt')
        cls._make_file('basic/dir1/file12')
        cls._make_file('basic/dir2/dir21/file211')
        cls._make_file('basic/dir2/file21')
        cls._make_file('basic/file1')
        cls._make_file('basic/file2.bin')

    def test_basic(self):
        self._test_make_rename_plan(
            u'basic',
            u'"file" "1"->"4"; "file42"->"dir3/file42"',
            (
                ('CreateDirectory', u'dir1/dir3'),
                ('MoveFile', u'dir1/file11.txt', u'dir1/file41.txt'),
                ('MoveFile', u'dir1/file12', u'dir1/dir3/file42'),
                ('MoveFile', u'file1', u'file4'),
                ('DeleteDirectoryIfEmpty', u'dir2/dir21'),
                ('DeleteDirectoryIfEmpty', u'dir2'),
                ('DeleteDirectoryIfEmpty', u'dir1'),
            ))

    @classmethod
    def setup_test_files_file_in_way(cls):
        cls._make_file('file_in_way/file1')
        cls._make_file('file_in_way/file2')
        cls._make_file('file_in_way/entry')

    def test_file_in_way_will_move(self):
        self._test_make_rename_plan(
            u'file_in_way',
            u'"entry"->"moved"; "file2"->"entry/file"',
            (
                ('MoveFile', u'entry', u'entry_1'),
                ('CreateDirectory', u'entry'),
                ('MoveFile', u'entry_1', u'moved'),
                ('MoveFile', u'file2', u'entry/file')
            ))

    def test_file_in_way_will_not_move(self):
        self._test_make_rename_plan(
            u'file_in_way',
            u'"file2"->"entry/file"',
            ('CannotCreateDestinationDirFileInTheWayWillNotMoveException', {'destination_dir': u'entry'}))

    def test_file_in_way_will_move_find_free_name(self):
        self._test_make_rename_plan(
            u'file_in_way',
            u'"file1"->"entry_1"; "entry"->"moved" $; "file2"->"entry/file"',
            (
                ('MoveFile', u'entry', u'entry_2'),
                ('CreateDirectory', u'entry'),
                ('MoveFile', u'file1', u'entry_1'),
                ('MoveFile', u'entry_2', u'moved'),
                ('MoveFile', u'file2', u'entry/file'),
            ))

    @classmethod
    def setup_test_files_chain(cls):
        cls._make_file('chain/file1')
        cls._make_file('chain/file2')
        cls._make_file('chain/file3')
        cls._make_file('chain/file4')

    def test_chain(self):
        self._test_make_rename_plan(
            u'chain',
            self._make_permutation_rules([2, 3, 4, 5]),
            (
                ('MoveFile', u'file4', u'file5'),
                ('MoveFile', u'file3', u'file4'),
                ('MoveFile', u'file2', u'file3'),
                ('MoveFile', u'file1', u'file2'),
            ))

    @classmethod
    def setup_test_files_circular(cls):
        cls._make_file('circular/file1')
        cls._make_file('circular/file2')
        cls._make_file('circular/file3')
        cls._make_file('circular/file4')

    def test_circular(self):
        self._test_make_rename_plan(
            u'circular',
            self._make_permutation_rules([2, 3, 4, 1]),
            (
                ('MoveFile', u'file3', u'file3_1'),
                ('MoveFile', u'file2', u'file3'),
                ('MoveFile', u'file1', u'file2'),
                ('MoveFile', u'file4', u'file1'),
                ('MoveFile', u'file3_1', u'file4')
            ))

    @classmethod
    def setup_test_files_complex_permutation(cls):
        cls._make_file('complex_perm/file1')
        cls._make_file('complex_perm/file2')
        cls._make_file('complex_perm/file3')
        cls._make_file('complex_perm/file4')
        cls._make_file('complex_perm/file5')
        cls._make_file('complex_perm/file6')
        cls._make_file('complex_perm/file7')
        cls._make_file('complex_perm/file8')

    def test_complex_permutation(self):
        self._test_make_rename_plan(
            u'complex_perm',
            self._make_permutation_rules([2, 10, 4, 5, 3, 7, 8, 9]),
            (
                ('MoveFile', u'file8', u'file9'),
                ('MoveFile', u'file7', u'file8'),
                ('MoveFile', u'file6', u'file7'),
                ('MoveFile', u'file2', u'file10'),
                ('MoveFile', u'file1', u'file2'),
                ('MoveFile', u'file3', u'file3_1'),
                ('MoveFile', u'file5', u'file3'),
                ('MoveFile', u'file4', u'file5'),
                ('MoveFile', u'file3_1', u'file4')
            ))

    def _test_make_rename_plan(self, base_dir, rules_text, expected_result):
        base_path = os.path.join(self._test_dir_path, base_dir)
        files = scan_files(base_path, recursive=True)
        rule_set = parse_rules(rules_text)
        renamed_files = rename_files(files, rule_set, use_path=False, use_extension=False)

        try:
            plan = make_rename_plan(base_path, renamed_files)
            result = plan.test_repr()
        except MakeRenamePlanException as e:
            result = e.test_repr()

        self.assertEquals(
            result,
            expected_result,
        )

    @staticmethod
    def _make_permutation_rules(permutation):
        return u'"file" ({0})'.format(u'|'.join(u'"{0}"->"{1}"'.format(i+1, p_i) for i, p_i in enumerate(permutation)))
