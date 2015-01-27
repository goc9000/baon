# baon/core/files/baon_paths.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


"""
Paths for scanned files in BAON have slightly different processing rules to those in os.path . This module provides
specialized functions for joining, splitting, extracting parts, etc. from these paths (which are always relative).
"""


import os


def all_path_components(path):
    return path.split(os.sep)


def all_path_components_no_empty(path):
    return all_path_components(path) if path != '' else []


def all_partial_paths(path):
    partial_paths = []
    partial_path = ''

    for component in all_path_components(path):
        partial_path = extend_path(partial_path, component)
        partial_paths.append(partial_path)

    return partial_paths


def join_path_components(components):
    return os.sep.join(components)


def extend_path(path, component):
    return path + os.sep + component if path != '' else component


def split_path_and_filename(path):
    path, _, filename = path.rpartition(os.sep)

    return path, filename


def split_path_head(path):
    head, _, remaining_path = path.partition(os.sep)

    return head, remaining_path
