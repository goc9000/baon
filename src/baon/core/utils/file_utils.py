# baon/core/file_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os


def all_path_components(path):
    components = []

    while path != '':
        head_path, last_component = os.path.split(path)
        if last_component != '':
            components.append(last_component)

        if path == head_path:
            components.append(head_path)
            break

        path = head_path

    components.reverse()

    return components


def enum_partial_paths(path):
    """
    Enumerates all non-empty parents of the given relative path, from the shortest to the longest.
    
    Does not work on absolute paths.
    """
    path, _ = os.path.split(path)
    
    base = ''
    
    if path != '':
        for comp in path.split(os.sep):
            base = os.path.join(base, comp)
            yield base
