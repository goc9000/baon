# baon/core/plan/make_rename_plan_new.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os
from collections import defaultdict
from itertools import count, chain

from baon.core.files.BAONPath import BAONPath
from baon.core.plan.RenamePlan import RenamePlan
from baon.core.plan.__errors__.make_rename_plan_errors import \
    RenamedFilesListHasErrorsError, \
    CannotRenameBasePathNotFoundError, \
    CannotRenameBasePathNotADirError, \
    CannotRenameNoPermissionsForBasePathError, \
    CannotCreateDestinationDirInaccessibleParentError, \
    CannotCreateDestinationDirUnexpectedNonDirParentError, \
    CannotCreateDestinationDirNoReadPermissionForParentError, \
    CannotCreateDestinationDirNoTraversePermissionForParentError, \
    CannotCreateDestinationDirNoWritePermissionForParentError, \
    CannotCreateDestinationDirFileInTheWayWillNotMoveError, \
    RenamedFilesListInvalidMultipleDestinationsError, \
    RenamedFilesListInvalidSameDestinationError, \
    CannotMoveFileNoWritePermissionForDirError
from baon.core.plan.actions.CreateDirectoryAction import CreateDirectoryAction
from baon.core.plan.actions.DeleteDirectoryIfEmptyAction import DeleteDirectoryIfEmptyAction
from baon.core.plan.actions.MoveFileAction import MoveFileAction


def make_rename_plan(renamed_files):
    return MakeRenamePlanInstance(renamed_files).run()


class MakeRenamePlanInstance(object):
    renamed_files = None
    steps = []

    def __init__(self, renamed_files):
        self.renamed_files = renamed_files

    def run(self):
        return RenamePlan(self.steps)

    # bail if there is nothing to do
#    if len(renamed_files) == 0:
#        return RenamePlan([])

#    _check_renamed_files_list(renamed_files)
#    _check_base_path(renamed_files)

#    taken_names_by_dir = _compute_taken_names_by_dir(renamed_files)

#    steps, created_dirs, nudges = _plan_creating_destination_dirs(renamed_files, taken_names_by_dir)
#    steps += _plan_moving_files(renamed_files, taken_names_by_dir, created_dirs, nudges)
#    steps += _plan_deleting_source_dirs(renamed_files)

#    return RenamePlan(steps)
