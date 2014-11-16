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


def extend_path(path, component):
    assert component != u''

    return path + os.sep + component if path != u'' else component


def split_path_and_filename(path):
    path, _, filename = path.rpartition(os.sep)

    return path, filename
