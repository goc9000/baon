# baon/core/plan/make_rename_plan.py
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
    BasePathNotFoundError, \
    BasePathNotADirError, \
    NoPermissionsForBasePathError, \
    CannotCreateDestinationDirInaccessibleParentError, \
    CannotCreateDestinationDirUnexpectedNonDirParentError, \
    CannotCreateDestinationDirNoReadPermissionForParentError, \
    CannotCreateDestinationDirNoWritePermissionForParentError, \
    CannotCreateDestinationDirFileInTheWayWillNotMoveError, \
    RenamedFilesListHasErrorsError, \
    RenamedFilesListInvalidMultipleDestinationsError, \
    RenamedFilesListInvalidSameDestinationError, \
    CannotMoveFileNoWritePermissionForDirError
from baon.core.plan.actions.CreateDirectoryAction import CreateDirectoryAction
from baon.core.plan.actions.DeleteDirectoryIfEmptyAction import DeleteDirectoryIfEmptyAction
from baon.core.plan.actions.MoveFileAction import MoveFileAction


def make_rename_plan(renamed_files):
    # bail if there is nothing to do
    if len(renamed_files) == 0:
        return RenamePlan([])

    _check_renamed_files_list(renamed_files)
    _check_base_path(renamed_files)

    taken_names_by_dir = _compute_taken_names_by_dir(renamed_files)

    steps, created_dirs, nudges = _plan_creating_destination_dirs(renamed_files, taken_names_by_dir)
    steps += _plan_moving_files(renamed_files, taken_names_by_dir, created_dirs, nudges)
    steps += _plan_deleting_source_dirs(renamed_files)

    return RenamePlan(steps)


def _check_renamed_files_list(renamed_files):
    BAONPath.assert_all_compatible(*(renamed_fref.path for renamed_fref in renamed_files))

    if any(renamed_fref.has_errors() for renamed_fref in renamed_files):
        raise RenamedFilesListHasErrorsError()


def _check_base_path(renamed_files):
    base_path = renamed_files[0].path.base_path

    if not os.path.exists(base_path):
        raise BasePathNotFoundError(base_path)
    if not os.path.isdir(base_path):
        raise BasePathNotADirError(base_path)
    if not os.access(base_path, os.R_OK | os.W_OK | os.X_OK):
        raise NoPermissionsForBasePathError(base_path)


def _compute_taken_names_by_dir(renamed_files):
    taken_names_by_dir = defaultdict(set)

    for f in renamed_files:
        for path in chain(f.path.subpaths(exclude_root=True), f.old_file_ref.path.subpaths(exclude_root=True)):
            taken_names_by_dir[path.parent_path()].add(path.basename())

    return taken_names_by_dir


def _plan_creating_destination_dirs(renamed_files, taken_names_by_dir):
    initial_paths = set([f.old_file_ref.path for f in renamed_files])
    final_paths = set([f.path for f in renamed_files])

    all_destination_dirs = set()
    for renamed_ref in renamed_files:
        all_destination_dirs.update(renamed_ref.path.parent_paths())

    actions = []
    created_dirs = set()
    nudges = dict()

    for path in sorted(all_destination_dirs):
        if path.is_root():
            continue

        parent_path, dir_name = path.parent_path(), path.basename()
        real_path = path.real_path()

        if parent_path not in created_dirs:
            real_parent_path = parent_path.real_path()

            if not os.path.exists(real_parent_path):
                raise CannotCreateDestinationDirInaccessibleParentError(path.path_text())
            if not os.path.isdir(real_parent_path):
                raise CannotCreateDestinationDirUnexpectedNonDirParentError(path.path_text())
            if not os.access(real_parent_path, os.R_OK | os.X_OK):
                raise CannotCreateDestinationDirNoReadPermissionForParentError(path.path_text())

            if os.path.exists(real_path) and os.path.isdir(real_path):
                continue

            if not os.access(real_parent_path, os.W_OK):
                raise CannotCreateDestinationDirNoWritePermissionForParentError(path.path_text())

            if os.path.exists(real_path) and not os.path.isdir(real_path):
                # A file is in the way. If it is scheduled to move, we will nudge it, i.e.
                # move it to a temporary alternate name in the same directory
                will_move = path in initial_paths and path not in final_paths
                if not will_move:
                    raise CannotCreateDestinationDirFileInTheWayWillNotMoveError(path.path_text())

                new_path = _nudge_file(path, taken_names_by_dir)
                nudges[path] = new_path

                actions.append(_move_file(path, new_path, created_dirs))

        actions.append(CreateDirectoryAction(real_path))
        created_dirs.add(path)

    return actions, created_dirs, nudges


def _nudge_file(path, taken_names_by_dir):
    parent_path, current_name = path.parent_path(), path.basename()

    taken_names = set(os.listdir(parent_path.real_path()))
    taken_names.update(taken_names_by_dir[parent_path])

    new_name = _coin_temporary_name(current_name, taken_names)
    new_path = path.replace_basename(new_name)

    taken_names_by_dir[parent_path].add(new_name)

    return new_path


def _coin_temporary_name(current_name, taken_names):
    for discriminant in count(1):
        new_name = "{0}_{1}".format(current_name, discriminant)

        if new_name not in taken_names:
            return new_name


def _move_file(from_path, to_path, created_dirs):
    for path in [from_path, to_path]:
        parent_path = path.parent_path()

        if parent_path in created_dirs:
            continue
        if not os.access(parent_path.real_path(), os.W_OK):
            raise CannotMoveFileNoWritePermissionForDirError(
                from_path.path_text(),
                to_path.path_text(),
                parent_path.path_text(),
            )

    return MoveFileAction(from_path.real_path(), to_path.real_path())


def _plan_moving_files(renamed_files, taken_names_by_dir, created_dirs, nudges):
    direct_arcs, reverse_arcs = _create_rename_graph(renamed_files, nudges)

    actions, cycle_nodes = _resolve_rename_chains(direct_arcs, reverse_arcs, created_dirs)
    actions += _resolve_cycles(cycle_nodes, reverse_arcs, taken_names_by_dir, created_dirs)

    return actions


def _create_rename_graph(renamed_files, nudges):
    """
    Create a graph where the nodes represent filenames, and arcs desired rename operations.
    Note: We expect that both internal and external degrees of any node will be limited to 1, because
    a file has only one destination, and there are no collisions.

    Returns a tuple of two dictionaries representing the direct and reverse arcs respectively.
    """
    direct_arcs = dict()
    reverse_arcs = dict()

    for f in renamed_files:
        source = f.old_file_ref.path
        if source in nudges:
            source = nudges[source]

        destination = f.path

        if source == destination:
            continue

        current_dest = direct_arcs.get(source)
        current_source = reverse_arcs.get(destination)

        if current_dest is not None and current_dest != destination:
            raise RenamedFilesListInvalidMultipleDestinationsError(
                source.path_text(),
                destination.path_text(),
                current_dest.path_text(),
            )
        if current_source is not None and current_source != source:
            raise RenamedFilesListInvalidSameDestinationError(
                destination.path_text(),
                source.path_text(),
                current_source.path_text(),
            )

        direct_arcs[source] = destination
        reverse_arcs[destination] = source

    return direct_arcs, reverse_arcs


def _resolve_rename_chains(direct_arcs, reverse_arcs, created_dirs):
    middle_nodes = set(a for a, b in direct_arcs.items() if a in reverse_arcs)
    end_nodes = set(b for a, b in direct_arcs.items() if b not in direct_arcs)

    actions = []

    # We use sorted() to make the algorithm deterministic
    for end_node in sorted(end_nodes):
        node = end_node
        while node in reverse_arcs:
            actions.append(_move_file(reverse_arcs[node], node, created_dirs))
            middle_nodes.discard(reverse_arcs[node])
            node = reverse_arcs[node]

    return actions, middle_nodes


def _resolve_cycles(cycle_nodes, reverse_arcs, taken_names_by_dir, created_dirs):
    actions = []

    resolved_nodes = set()

    # We use sorted() to make the algorithm deterministic
    for start_node in sorted(cycle_nodes):
        if start_node in resolved_nodes:
            continue

        temp_node = _nudge_file(start_node, taken_names_by_dir)
        actions.append(_move_file(start_node, temp_node, created_dirs))

        node = start_node
        while reverse_arcs[node] != start_node:
            parent_node = reverse_arcs[node]
            resolved_nodes.add(parent_node)

            actions.append(_move_file(parent_node, node, created_dirs))

            node = parent_node

        actions.append(_move_file(temp_node, node, created_dirs))

    return actions


def _plan_deleting_source_dirs(renamed_files):
    all_source_dirs = set()
    for renamed_ref in renamed_files:
        all_source_dirs.update(renamed_ref.old_file_ref.path.parent_paths())

    return [
        DeleteDirectoryIfEmptyAction(path.real_path())
        for path in reversed(sorted(all_source_dirs))
        if not path.is_root()
    ]
