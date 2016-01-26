# baon/core/plan/__tests__/test_make_rename_plan_case_insensitive.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.__tests__.FileSystemTestCase import requires_case_insensitive_filesystem
from baon.core.plan.__tests__.MakeRenamePlanTestCaseBase import MakeRenamePlanTestCaseBase


class TestMakeRenamePlanCaseInsensitive(MakeRenamePlanTestCaseBase):

    @requires_case_insensitive_filesystem
    def test_change_case_file(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'file', 'FILE'),
            ),
            (
                ('CreateDirectory', '<STAGING_DIR>'),
                ('MoveFile', 'file', '<STAGING_DIR>/FILE'),
                ('MoveFile', '<STAGING_DIR>/FILE', 'FILE'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>'),
            ),
        )

    @requires_case_insensitive_filesystem
    def test_change_case_dir(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'dir/file', 'DIR/file'),
            ),
            (
                ('CreateDirectory', '<STAGING_DIR>'),
                ('CreateDirectory', '<STAGING_DIR>/DIR'),
                ('MoveFile', 'dir/file', '<STAGING_DIR>/DIR/file'),
                ('DeleteEmptyDirectory', 'dir'),
                ('MoveFile', '<STAGING_DIR>/DIR/file', 'DIR/file'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>/DIR'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>'),
            ),
        )

    @requires_case_insensitive_filesystem
    def test_case_insensitive_source_collision(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'ABC', 'def'),
                ('FILE', 'abc', 'efg'),
            ),
            ('CaseInsensitiveConflictInSourcePathsError', {'path_1': 'ABC', 'path_2': 'abc'}),
        )

    @requires_case_insensitive_filesystem
    def test_case_insensitive_source_collision_in_case_sensitive_filesystem(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'ABC', 'def'),
                ('FILE', 'abc', 'efg'),
            ),
            (
                ('CreateDirectory', '<STAGING_DIR>'),
                ('MoveFile', 'ABC', '<STAGING_DIR>/def'),
                ('MoveFile', 'abc', '<STAGING_DIR>/efg'),
                ('MoveFile', '<STAGING_DIR>/def', 'def'),
                ('MoveFile', '<STAGING_DIR>/efg', 'efg'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>'),
            ),
            case_insensitive_override=False,
        )

    @requires_case_insensitive_filesystem
    def test_case_insensitive_dir_source_collision(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'ABC/def', 'ABC/ghi'),
                ('FILE', 'abc/ghi', 'abc/jkl'),
            ),
            ('CaseInsensitiveConflictInSourcePathsError', {'path_1': 'ABC', 'path_2': 'abc'}),
        )

    @requires_case_insensitive_filesystem
    def test_case_insensitive_dir_source_collision_in_case_sensitive_filesystem(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'ABC/def', 'ABC/ghi'),
                ('FILE', 'abc/ghi', 'abc/efg'),
            ),
            (
                ('CreateDirectory', '<STAGING_DIR>'),
                ('CreateDirectory', '<STAGING_DIR>/ABC'),
                ('CreateDirectory', '<STAGING_DIR>/abc'),
                ('MoveFile', 'ABC/def', '<STAGING_DIR>/ABC/ghi'),
                ('MoveFile', 'abc/ghi', '<STAGING_DIR>/abc/efg'),
                ('MoveFile', '<STAGING_DIR>/ABC/ghi', 'ABC/ghi'),
                ('MoveFile', '<STAGING_DIR>/abc/efg', 'abc/efg'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>/abc'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>/ABC'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>'),
            ),
            case_insensitive_override=False,
        )

    @requires_case_insensitive_filesystem
    def test_case_insensitive_dest_collision(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'abc', 'ABCdef'),
                ('FILE', 'def', 'abcDEF'),
            ),
            ('CaseInsensitiveConflictInDestinationPathsError', {'path_1': 'ABCdef', 'path_2': 'abcDEF'}),
        )

    @requires_case_insensitive_filesystem
    def test_no_case_insensitive_dest_collision_in_case_sensitive_filesystem(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'abc', 'ABCdef'),
                ('FILE', 'def', 'abcDEF'),
            ),
            (
                ('CreateDirectory', '<STAGING_DIR>'),
                ('MoveFile', 'abc', '<STAGING_DIR>/ABCdef'),
                ('MoveFile', 'def', '<STAGING_DIR>/abcDEF'),
                ('MoveFile', '<STAGING_DIR>/ABCdef', 'ABCdef'),
                ('MoveFile', '<STAGING_DIR>/abcDEF', 'abcDEF'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>'),
            ),
            case_insensitive_override=False,
        )

    @requires_case_insensitive_filesystem
    def test_case_insensitive_dir_dest_collision(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'abc/def', 'ABC/def'),
                ('FILE', 'abc/ghi', 'abc/kkk'),
            ),
            ('CaseInsensitiveConflictInDestinationPathsError', {'path_1': 'ABC', 'path_2': 'abc'}),
        )

    @requires_case_insensitive_filesystem
    def test_no_case_insensitive_dir_dest_collision_in_case_sensitive_filesystem(self):
        self._test_make_rename_plan(
            (
                ('FILE', 'abc/def', 'ABC/def'),
                ('FILE', 'abc/ghi', 'abc/kkk'),
            ),
            (
                ('CreateDirectory', '<STAGING_DIR>'),
                ('CreateDirectory', '<STAGING_DIR>/ABC'),
                ('CreateDirectory', '<STAGING_DIR>/abc'),
                ('MoveFile', 'abc/def', '<STAGING_DIR>/ABC/def'),
                ('MoveFile', 'abc/ghi', '<STAGING_DIR>/abc/kkk'),
                ('DeleteEmptyDirectory', 'abc'),
                ('CreateDirectory', 'abc'),
                ('MoveFile', '<STAGING_DIR>/ABC/def', 'ABC/def'),
                ('MoveFile', '<STAGING_DIR>/abc/kkk', 'abc/kkk'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>/abc'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>/ABC'),
                ('DeleteEmptyDirectory', '<STAGING_DIR>'),
            ),
            case_insensitive_override=False,
        )
