# baon/core/plan/make_rename_plan.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from collections import defaultdict
from itertools import count

from baon.core.files.baon_paths import all_partial_paths, split_path_and_filename, extend_path

from baon.core.plan.__errors__.make_rename_plan_errors import \
    CannotCreateDestinationDirInaccessibleParentError, \
    CannotCreateDestinationDirUnexpectedNonDirParentError, \
    CannotCreateDestinationDirNoReadPermissionForParentError, \
    CannotCreateDestinationDirNoTraversePermissionForParentError, \
    CannotCreateDestinationDirNoWritePermissionForParentError, \
    CannotCreateDestinationDirFileInTheWayWillNotMoveError, \
    RenamedFilesListInvalidMultipleDestinationsError, \
    RenamedFilesListInvalidSameDestinationError, \
    CannotMoveFileNoWritePermissionForDirError

from baon.core.plan.RenamePlan import RenamePlan
from baon.core.plan.actions.CreateDirectoryAction import CreateDirectoryAction
from baon.core.plan.actions.MoveFileAction import MoveFileAction
from baon.core.plan.actions.DeleteDirectoryIfEmptyAction import DeleteDirectoryIfEmptyAction


def make_rename_plan(base_path, renamed_files):
    taken_names_by_dir = _compute_taken_names_by_dir(renamed_files)

    steps, created_dirs, nudges = _plan_creating_destination_dirs(base_path, renamed_files, taken_names_by_dir)
    steps += _plan_moving_files(base_path, renamed_files, taken_names_by_dir, created_dirs, nudges)
    steps += _plan_deleting_source_dirs(renamed_files)

    return RenamePlan(steps)


def _compute_taken_names_by_dir(renamed_files):
    taken_names_by_dir = defaultdict(set)

    for f in renamed_files:
        for partial_path in all_partial_paths(f.filename) + all_partial_paths(f.old_file_ref.filename):
            dest_dir, new_entry = split_path_and_filename(partial_path)
            taken_names_by_dir[dest_dir].add(new_entry)

    return taken_names_by_dir


def _plan_creating_destination_dirs(base_path, renamed_files, taken_names_by_dir):
    initial_paths = set([f.old_file_ref.filename for f in renamed_files])
    final_paths = set([f.filename for f in renamed_files])

    all_destination_dirs = set()
    for renamed_ref in renamed_files:
        all_destination_dirs.update(all_partial_paths(renamed_ref.filename)[:-1])

    actions = []
    created_dirs = set()
    nudges = dict()

    for path in sorted(all_destination_dirs):
        parent_path, dir_name = split_path_and_filename(path)

        if parent_path not in created_dirs:
            real_path = os.path.join(base_path, path)
            real_parent_path = os.path.join(base_path, parent_path)

            if not os.path.exists(real_parent_path):
                raise CannotCreateDestinationDirInaccessibleParentError(path)
            if not os.path.isdir(real_parent_path):
                raise CannotCreateDestinationDirUnexpectedNonDirParentError(path)
            if not os.access(real_parent_path, os.R_OK):
                raise CannotCreateDestinationDirNoReadPermissionForParentError(path)
            if not os.access(real_parent_path, os.X_OK):
                raise CannotCreateDestinationDirNoTraversePermissionForParentError(path)

            if os.path.exists(real_path) and os.path.isdir(real_path):
                continue

            if not os.access(real_parent_path, os.W_OK):
                raise CannotCreateDestinationDirNoWritePermissionForParentError(path)

            if os.path.exists(real_path) and not os.path.isdir(real_path):
                # A file is in the way. If it is scheduled to move, we will nudge it, i.e.
                # move it to a temporary alternate name in the same directory
                will_move = path in initial_paths and path not in final_paths
                if not will_move:
                    raise CannotCreateDestinationDirFileInTheWayWillNotMoveError(path)

                new_path = _nudge_file(path, base_path, taken_names_by_dir)
                nudges[path] = new_path

                actions.append(_move_file(path, new_path, base_path, created_dirs))

        actions.append(CreateDirectoryAction(path))
        created_dirs.add(path)

    return actions, created_dirs, nudges


def _nudge_file(path, base_path, taken_names_by_dir):
    parent_path, current_name = split_path_and_filename(path)

    taken_names = set(os.listdir(os.path.join(base_path, parent_path)))
    taken_names.update(taken_names_by_dir[parent_path])

    new_name = _coin_temporary_name(current_name, taken_names)
    new_path = extend_path(parent_path, new_name)

    taken_names_by_dir[parent_path].add(new_name)

    return new_path


def _coin_temporary_name(current_name, taken_names):
    for discriminant in count(1):
        new_name = "{0}_{1}".format(current_name, discriminant)

        if new_name not in taken_names:
            return new_name


def _move_file(from_path, to_path, base_path, created_dirs):
    for path in [from_path, to_path]:
        parent_path, _ = split_path_and_filename(path)

        if parent_path in created_dirs:
            continue
        if not os.access(os.path.join(base_path, parent_path), os.W_OK):
            raise CannotMoveFileNoWritePermissionForDirError(from_path, to_path, parent_path)

    return MoveFileAction(from_path, to_path)


def _plan_moving_files(base_path, renamed_files, taken_names_by_dir, created_dirs, nudges):
    direct_arcs, reverse_arcs = _create_rename_graph(renamed_files, nudges)

    actions, cycle_nodes = _resolve_rename_chains(direct_arcs, reverse_arcs, base_path, created_dirs)
    actions += _resolve_cycles(cycle_nodes, reverse_arcs, base_path, taken_names_by_dir, created_dirs)

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
        source = f.old_file_ref.filename
        if source in nudges:
            source = nudges[source]

        destination = f.filename

        if source == destination:
            continue

        current_dest = direct_arcs.get(source)
        current_source = reverse_arcs.get(destination)

        if current_dest is not None and current_dest != destination:
            raise RenamedFilesListInvalidMultipleDestinationsError(source, destination, current_dest)
        if current_source is not None and current_source != source:
            raise RenamedFilesListInvalidSameDestinationError(destination, source, current_source)

        direct_arcs[source] = destination
        reverse_arcs[destination] = source

    return direct_arcs, reverse_arcs


def _resolve_rename_chains(direct_arcs, reverse_arcs, base_path, created_dirs):
    middle_nodes = set(a for a, b in direct_arcs.items() if a in reverse_arcs)
    end_nodes = set(b for a, b in direct_arcs.items() if b not in direct_arcs)

    actions = []

    # We use sorted() to make the algorithm deterministic
    for end_node in sorted(end_nodes):
        node = end_node
        while node in reverse_arcs:
            actions.append(_move_file(reverse_arcs[node], node, base_path, created_dirs))
            middle_nodes.discard(reverse_arcs[node])
            node = reverse_arcs[node]

    return actions, middle_nodes


def _resolve_cycles(cycle_nodes, reverse_arcs, base_path, taken_names_by_dir, created_dirs):
    actions = []

    resolved_nodes = set()

    # We use sorted() to make the algorithm deterministic
    for start_node in sorted(cycle_nodes):
        if start_node in resolved_nodes:
            continue

        temp_node = _nudge_file(start_node, base_path, taken_names_by_dir)
        actions.append(_move_file(start_node, temp_node, base_path, created_dirs))

        node = start_node
        while reverse_arcs[node] != start_node:
            parent_node = reverse_arcs[node]
            resolved_nodes.add(parent_node)

            actions.append(_move_file(parent_node, node, base_path, created_dirs))

            node = parent_node

        actions.append(_move_file(temp_node, node, base_path, created_dirs))

    return actions


def _plan_deleting_source_dirs(renamed_files):
    all_source_dirs = set()
    for renamed_ref in renamed_files:
        all_source_dirs.update(all_partial_paths(renamed_ref.old_file_ref.filename)[:-1])

    return [DeleteDirectoryIfEmptyAction(path) for path in reversed(sorted(all_source_dirs))]
