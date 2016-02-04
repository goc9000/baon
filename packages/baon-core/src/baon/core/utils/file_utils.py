# baon/core/file_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os
import stat


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


def set_file_rights(path, read=None, write=None, execute=None):
    def adjust_bits(mode, bitmask, condition):
        if condition is True:
            return mode | bitmask
        elif condition is False:
            return mode & ~bitmask
        else:
            return mode

    current_mode = os.lstat(path).st_mode

    current_mode = adjust_bits(current_mode, stat.S_IRUSR, read)
    current_mode = adjust_bits(current_mode, stat.S_IWUSR, write)
    current_mode = adjust_bits(current_mode, stat.S_IXUSR, execute)

    os.lchmod(path, current_mode)


def check_file_rights(path, read=None, write=None, execute=None):
    return (
        ((read is None) or (os.access(path, os.R_OK) == read)) and
        ((write is None) or (os.access(path, os.W_OK) == write)) and
        ((execute is None) or (os.access(path, os.X_OK) == execute))
    )
