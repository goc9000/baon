# baon/core/plan/make_rename_plan_new.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os
from itertools import count

from baon.core.files.BAONPath import BAONPath
from baon.core.plan.RenamePlan import RenamePlan
from baon.core.plan.__errors__.make_rename_plan_errors import \
    BasePathNotFoundError, \
    BasePathNotADirError, \
    NoPermissionsForBasePathError, \
    CannotMoveFileNoWritePermissionForDirError, \
    RenamedFilesListHasErrorsError, \
    RenamedFilesListInvalidMultipleDestinationsError, \
    RenamedFilesListInvalidSameDestinationError
from baon.core.plan.actions.CreateDirectoryAction import CreateDirectoryAction
from baon.core.plan.actions.DeleteEmptyDirectoryAction import DeleteEmptyDirectoryAction
from baon.core.plan.actions.MoveFileAction import MoveFileAction
from baon.core.utils.lang_utils import sets_union


STAGING_DIR_PATTERN = 'TMP_BAON_STAGING{0}'


def make_rename_plan(renamed_files):
    return MakeRenamePlanInstance(renamed_files).run()


def staging_dir_variants():
    yield STAGING_DIR_PATTERN.format('')

    for x in count(1):
        yield STAGING_DIR_PATTERN.format(x)


class MakeRenamePlanInstance(object):
    renamed_files = None
    base_path = None
    staging_dir = None
    staging_structure = None
    steps = None

    def __init__(self, renamed_files):
        self.renamed_files = renamed_files
        self.steps = []

    def run(self):
        self._keep_only_changed_files()
        if len(self.renamed_files) > 0:
            self._check_renamed_files_list()
            self._compute_base_path()
            self._check_base_path()

            self._choose_name_for_staging_dir()

            self._phase1_create_staging_structure()
            self._phase2_move_files_to_staging()
            self._phase6_tear_down_staging_structure()

        return RenamePlan(self.steps)

    def _keep_only_changed_files(self):
        self.renamed_files = [f for f in self.renamed_files if f.is_changed()]

    def _check_renamed_files_list(self):
        BAONPath.assert_all_compatible(*(renamed_fref.path for renamed_fref in self.renamed_files))

        if any(renamed_fref.has_errors() for renamed_fref in self.renamed_files):
            raise RenamedFilesListHasErrorsError()

        by_source = {}
        by_destination = {}

        for renamed_fref in self.renamed_files:
            source = renamed_fref.old_file_ref.path
            destination = renamed_fref.path

            if source in by_source:
                raise RenamedFilesListInvalidMultipleDestinationsError(
                    source.path_text(),
                    by_source[source].path_text(),
                    destination.path_text(),
                )
            if destination in by_destination:
                raise RenamedFilesListInvalidSameDestinationError(
                    destination.path_text(),
                    by_destination[destination].path_text(),
                    source.path_text(),
                )

            by_source[source] = destination
            by_destination[destination] = source

    def _compute_base_path(self):
        self.base_path = self.renamed_files[0].path.base_path

    def _check_base_path(self):
        if not os.path.exists(self.base_path):
            raise BasePathNotFoundError(self.base_path)
        if not os.path.isdir(self.base_path):
            raise BasePathNotADirError(self.base_path)
        if not os.access(self.base_path, os.R_OK | os.W_OK | os.X_OK):
            raise NoPermissionsForBasePathError(self.base_path)

    def _choose_name_for_staging_dir(self):
        taken_names_in_base = set(
            os.listdir(self.base_path) +
            [f.path.components[0] for f in self.renamed_files] +
            [f.old_file_ref.path.components[0] for f in self.renamed_files]
        )

        # fold case to account for case-insensitive filesystems
        taken_names_in_base = set(x.lower() for x in taken_names_in_base)

        for staging_dir in staging_dir_variants():
            if staging_dir.lower() not in taken_names_in_base:
                self.staging_dir = staging_dir
                return

    def _phase1_create_staging_structure(self):
        destination_parent_paths = sets_union(f.path.parent_paths() for f in self.renamed_files)
        self.staging_structure = sorted(self._path_to_staging_dir(path) for path in destination_parent_paths)

        self.steps.extend(CreateDirectoryAction(path.real_path()) for path in self.staging_structure)

    def _path_to_staging_dir(self, path):
        return BAONPath(path.base_path, [self.staging_dir] + path.components)

    def _phase2_move_files_to_staging(self):
        for renamed_fref in self.renamed_files:
            from_path = renamed_fref.old_file_ref.path
            to_path = self._path_to_staging_dir(renamed_fref.path)

            if not os.access(from_path.parent_path().real_path(), os.W_OK):
                raise CannotMoveFileNoWritePermissionForDirError(
                    from_path.path_text(),
                    to_path.path_text(),
                    from_path.parent_path().path_text(),
                )

            self.steps.append(MoveFileAction(from_path.real_path(), to_path.real_path()))

    def _phase6_tear_down_staging_structure(self):
        self.steps.extend(DeleteEmptyDirectoryAction(path.real_path()) for path in reversed(self.staging_structure))
