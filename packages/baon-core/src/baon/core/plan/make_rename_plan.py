# baon/core/plan/make_rename_plan_new.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os
from collections import defaultdict
from itertools import count

from baon.core.files.BAONPath import BAONPath
from baon.core.plan.RenamePlan import RenamePlan
from baon.core.plan.__errors__.make_rename_plan_errors import \
    BasePathNotFoundError, \
    BasePathNotADirError, \
    NoPermissionsForBasePathError, \
    CannotScanDirectoryError, \
    CannotMoveFileNoWritePermissionForDirError, \
    CannotCreateDestinationDirInaccessibleParentError, \
    CannotCreateDestinationDirUnexpectedNonDirParentError, \
    CannotCreateDestinationDirNoReadPermissionForParentError, \
    CannotCreateDestinationDirNoWritePermissionForParentError, \
    CannotCreateDestinationDirFileInTheWayWillNotMoveError, \
    RenamedFilesListHasErrorsError, \
    RenamedFilesListInvalidMultipleDestinationsError, \
    RenamedFilesListInvalidSameDestinationError, \
    CaseInsensitiveConflictInSourcePathsError, \
    CaseInsensitiveConflictInDestinationPathsError
from baon.core.plan.actions.CreateDirectoryAction import CreateDirectoryAction
from baon.core.plan.actions.DeleteEmptyDirectoryAction import DeleteEmptyDirectoryAction
from baon.core.plan.actions.MoveFileAction import MoveFileAction
from baon.core.utils.file_utils import check_filesystem_at_path_case_insensitive, check_file_rights
from baon.core.utils.lang_utils import sets_union, pairwise

STAGING_DIR_PATTERN = 'TMP_BAON_STAGING{0}'


def make_rename_plan(*args, **kwargs):
    return MakeRenamePlanInstance(*args, **kwargs).run()


def staging_dir_variants():
    yield STAGING_DIR_PATTERN.format('')

    for x in count(1):
        yield STAGING_DIR_PATTERN.format(x)


class MakeRenamePlanInstance(object):
    # Inputs
    renamed_files = None
    case_insensitive_filesystem = None

    # Cached
    base_path = None
    staging_dir = None
    destination_dirs = None
    staging_structure = None
    removed_entries_by_path = None
    created_dirs = None

    # Outputs
    steps = None

    def __init__(self, renamed_files, case_insensitive_filesystem=None):
        self.renamed_files = renamed_files
        self.case_insensitive_filesystem = case_insensitive_filesystem
        self.steps = []

    def run(self):
        self._keep_only_changed_files()
        if len(self.renamed_files) > 0:
            self._compute_base_path()
            self._check_base_path()
            self._set_case_insensitive()
            self._check_renamed_files_list()

            self._choose_name_for_staging_dir()

            self._phase1_create_staging_structure()
            self._phase2_move_files_to_staging()
            self._phase3_delete_emptied_directories()
            self._phase4_create_destination_directories()
            self._phase5_move_files_to_final_destination()
            self._phase6_tear_down_staging_structure()

        return RenamePlan(self.steps)

    def _keep_only_changed_files(self):
        self.renamed_files = [f for f in self.renamed_files if f.is_changed()]

    def _check_renamed_files_list(self):
        BAONPath.assert_all_compatible(*(renamed_fref.path for renamed_fref in self.renamed_files))

        if any(renamed_fref.has_errors() for renamed_fref in self.renamed_files):
            raise RenamedFilesListHasErrorsError()

        self._check_case_sensitive_sources_destinations()

        if self.case_insensitive_filesystem:
            self._check_case_insensitive_sources_destinations()

    def _check_case_sensitive_sources_destinations(self):
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

    def _check_case_insensitive_sources_destinations(self):
        key_getter = lambda path: ([component.lower() for component in path.components], path)

        source_paths = sets_union([f.old_file_ref.path.subpaths(exclude_root=True) for f in self.renamed_files])
        for path_a, path_b in pairwise(sorted(source_paths, key=key_getter)):
            if path_a.equals_ignore_case(path_b):
                raise CaseInsensitiveConflictInSourcePathsError(path_a.path_text(), path_b.path_text())

        destination_paths = sets_union([f.path.subpaths(exclude_root=True) for f in self.renamed_files])
        for path_a, path_b in pairwise(sorted(destination_paths, key=key_getter)):
            if path_a.equals_ignore_case(path_b):
                raise CaseInsensitiveConflictInDestinationPathsError(path_a.path_text(), path_b.path_text())

    def _compute_base_path(self):
        self.base_path = self.renamed_files[0].path.base_path

    def _check_base_path(self):
        if not os.path.exists(self.base_path):
            raise BasePathNotFoundError(self.base_path)
        if not os.path.isdir(self.base_path):
            raise BasePathNotADirError(self.base_path)
        if not check_file_rights(self.base_path, read=True, write=True, execute=True):
            raise NoPermissionsForBasePathError(self.base_path)

    def _set_case_insensitive(self):
        if self.case_insensitive_filesystem is None:
            self.case_insensitive_filesystem = check_filesystem_at_path_case_insensitive(self.base_path)

    def _choose_name_for_staging_dir(self):
        taken_names_in_base = set(
            self._list_dir(self.base_path) +
            [f.path.components[0] for f in self.renamed_files] +
            [f.old_file_ref.path.components[0] for f in self.renamed_files]
        )

        # fold case to account for case-insensitive filesystems
        taken_names_in_base = set(x.lower() for x in taken_names_in_base)

        for staging_dir in staging_dir_variants():
            if staging_dir.lower() not in taken_names_in_base:
                self.staging_dir = staging_dir
                return

    def _list_dir(self, real_path):
        try:
            return os.listdir(real_path)
        except OSError as e:
            raise CannotScanDirectoryError(real_path) from e

    def _phase1_create_staging_structure(self):
        self.destination_dirs = sorted(sets_union(f.path.parent_paths() for f in self.renamed_files))
        self.staging_structure = sorted(self._path_to_staging_dir(path) for path in self.destination_dirs)

        self.steps.extend(CreateDirectoryAction(path.real_path()) for path in self.staging_structure)

    def _path_to_staging_dir(self, path):
        return BAONPath(path.base_path, [self.staging_dir] + path.components)

    def _phase2_move_files_to_staging(self):
        self.removed_entries_by_path = defaultdict(set)

        for renamed_fref in self.renamed_files:
            from_path = renamed_fref.old_file_ref.path
            to_path = self._path_to_staging_dir(renamed_fref.path)

            if not check_file_rights(from_path.parent_path().real_path(), read=True, write=True, execute=True):
                raise CannotMoveFileNoWritePermissionForDirError(
                    from_path.path_text(),
                    to_path.path_text(),
                    from_path.parent_path().path_text(),
                )

            self.steps.append(MoveFileAction(from_path.real_path(), to_path.real_path()))
            self.removed_entries_by_path[from_path.parent_path()].add(from_path.basename())

    def _phase3_delete_emptied_directories(self):
        source_parent_paths = sets_union(
            f.old_file_ref.path.subpaths(exclude_root=True, exclude_self=True)
            for f in self.renamed_files
        )

        undeletable_dirs = set()

        for path in reversed(sorted(source_parent_paths)):
            if path in undeletable_dirs:
                continue

            files_in_dir = set(self._list_dir(path.real_path()))
            if path in self.removed_entries_by_path:
                files_in_dir -= self.removed_entries_by_path[path]

            if len(files_in_dir) == 0 and \
                    check_file_rights(path.parent_path().real_path(), read=True, write=True, execute=True):
                self.steps.append(DeleteEmptyDirectoryAction(path.real_path()))
                self.removed_entries_by_path[path.parent_path()].add(path.basename())
            else:
                undeletable_dirs |= set(path.subpaths(exclude_root=True, exclude_self=True))

    def _phase4_create_destination_directories(self):
        self.created_dirs = set()

        for path in self.destination_dirs:
            if path.is_root():
                continue

            if path.is_root() or path.parent_path() in self.created_dirs:
                pass
            elif self._is_path_removed(path.parent_path()) or not os.path.exists(path.parent_path().real_path()):
                raise CannotCreateDestinationDirInaccessibleParentError(path.path_text())
            elif not os.path.isdir(path.parent_path().real_path()):
                raise CannotCreateDestinationDirUnexpectedNonDirParentError(path.path_text())
            elif not check_file_rights(path.parent_path().real_path(), read=True, execute=True):
                raise CannotCreateDestinationDirNoReadPermissionForParentError(path.path_text())

            if self._is_path_removed(path) or not os.path.exists(path.real_path()):
                if not check_file_rights(path.parent_path().real_path(), write=True):
                    raise CannotCreateDestinationDirNoWritePermissionForParentError(path.path_text())

                self.steps.append(CreateDirectoryAction(path.real_path()))
                self.created_dirs.add(path)
                self.removed_entries_by_path[path.parent_path()].discard(path.basename())
                continue

            if path in self.created_dirs or os.path.isdir(path.real_path()):
                continue  # already created

            raise CannotCreateDestinationDirFileInTheWayWillNotMoveError(path.path_text())

    def _is_path_removed(self, path):
        return (
            (not path.is_root()) and
            (path.parent_path() in self.removed_entries_by_path) and
            (path.basename() in self.removed_entries_by_path[path.parent_path()])
        )

    def _phase5_move_files_to_final_destination(self):
        for renamed_fref in self.renamed_files:
            from_path = self._path_to_staging_dir(renamed_fref.path)
            to_path = renamed_fref.path

            if (
                (not to_path.is_root()) and
                (to_path.parent_path() not in self.created_dirs) and
                (not check_file_rights(to_path.parent_path().real_path(), write=True))
            ):
                raise CannotMoveFileNoWritePermissionForDirError(
                    from_path.path_text(),
                    to_path.path_text(),
                    from_path.parent_path().path_text(),
                )

            self.steps.append(MoveFileAction(from_path.real_path(), to_path.real_path()))

    def _phase6_tear_down_staging_structure(self):
        self.steps.extend(DeleteEmptyDirectoryAction(path.real_path()) for path in reversed(self.staging_structure))
