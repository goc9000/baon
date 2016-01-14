# baon/core/file_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os


def check_filesystem_at_path_case_insensitive(path):
    """
    Checks whether the file system at the specified path is case insensitive. The path must exist.

    Note that the function is not completely correct, as we are trying to perform the check without creating a
    temporary file (which introduces additional failure cases itself if we don't have permissions). It will fail if
    all the components of the absolute path are non-alphabetic, which should be quite rare as on Windows we start
    with a drive letter, while on OS X and Linux, the toplevel dirs are somewhat standardized (/var, /usr etc).
    """
    full_path = os.path.abspath(path)

    assert os.path.exists(full_path), 'Checking case insensitivity for non-existent path'

    return os.path.exists(full_path.swapcase())
