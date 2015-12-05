# baon/core/plan/make_rename_plan_new.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.files.BAONPath import BAONPath
from baon.core.plan.RenamePlan import RenamePlan
from baon.core.plan.__errors__.make_rename_plan_errors import \
    RenamedFilesListHasErrorsError,\
    CannotRenameBasePathNotFoundError,\
    CannotRenameBasePathNotADirError,\
    CannotRenameNoPermissionsForBasePathError


def make_rename_plan(renamed_files):
    return MakeRenamePlanInstance(renamed_files).run()


class MakeRenamePlanInstance(object):
    renamed_files = None
    base_path = None
    steps = []

    def __init__(self, renamed_files):
        self.renamed_files = renamed_files

    def run(self):
        self._keep_only_changed_files()
        if len(self.renamed_files) > 0:
            self._check_renamed_files_list()
            self._compute_base_path()
            self._check_base_path()

        return RenamePlan(self.steps)

    def _keep_only_changed_files(self):
        self.renamed_files = [f for f in self.renamed_files if f.is_changed()]

    def _check_renamed_files_list(self):
        BAONPath.assert_all_compatible(*(renamed_fref.path for renamed_fref in self.renamed_files))

        if any(renamed_fref.has_errors() for renamed_fref in self.renamed_files):
            raise RenamedFilesListHasErrorsError()

    def _compute_base_path(self):
        self.base_path = self.renamed_files[0].path.base_path

    def _check_base_path(self):
        if not os.path.exists(self.base_path):
            raise CannotRenameBasePathNotFoundError(self.base_path)
        if not os.path.isdir(self.base_path):
            raise CannotRenameBasePathNotADirError(self.base_path)
        if not os.access(self.base_path, os.R_OK | os.W_OK | os.X_OK):
            raise CannotRenameNoPermissionsForBasePathError(self.base_path)
