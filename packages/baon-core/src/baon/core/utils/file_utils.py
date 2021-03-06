# baon/core/file_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os
import platform
import stat
import tempfile

from collections import namedtuple
from functools import lru_cache

from baon.core.utils.windows_utils import on_windows, permissions_supported


FileInfo = namedtuple('FileInfo', ['is_dir', 'is_link', 'stat_info'])


@lru_cache()
def check_default_filesystem_case_insensitive():
    """
    Checks whether the default file system used in the current OS is case insensitive.

    This function is cached.
    """
    with tempfile.NamedTemporaryFile(prefix="TEMP") as f:
        return os.path.exists(f.name.swapcase())


@lru_cache()
def check_default_filesystem_supports_links():
    """
    Checks whether the default file system supports symbolic links.

    This function is cached.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        full_link_path = os.path.join(tmp_dir, 'temp_link')
        full_target_path = tmp_dir

        try:
            os.symlink(full_target_path, full_link_path)
        except OSError:
            return False

        os.unlink(full_link_path)

        return True


def check_default_filesystem_is_posix():
    """
    Checks whether the default file system is POSIX (and thus POSIX permissions make sense for it)
    """
    return platform.system() in ['Linux', 'Darwin']


def check_default_filesystem_supports_permissions():
    """
    Checks whether the default file systems supports at least basic file permissions AND that BAON is equipped to
    set permissions in that environment.
    """
    if check_default_filesystem_is_posix():
        return True
    if on_windows():
        return permissions_supported()

    return False


def check_default_filesystem_supports_unicode():
    """
    Checks whether the default file system supports Unicode filenames.
    """
    return os.path.supports_unicode_filenames


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


def stat_file(path):
    """
    Gets information on a path entry. Returns a named tuple containing the fields:
    - is_dir: True if the file is a directory (or a link pointing to a directory)
    - is_link: True if the file is a symbolic link
    - stat_info: Info reported by lstat (mode, etc.)

    Unlike Python's standard functions, this will throw FileNotFound or PermissionError if the path does not exist
    or cannot be accessed due to permissions issues.
    """
    return FileInfo(
        is_dir=os.path.isdir(path),
        is_link=os.path.islink(path),
        stat_info=os.lstat(path),
    )


def set_file_rights(path, read=None, write=None, execute=None, traverse=None):
    def adjust_bits(mode, bitmask, condition):
        if condition is True:
            return mode | bitmask
        elif condition is False:
            return mode & ~bitmask
        else:
            return mode

    file_info = stat_file(path)
    current_mode = file_info.stat_info.st_mode

    assert execute is None or not file_info.is_dir, 'The execute permission applies only to files'
    assert traverse is None or file_info.is_dir, 'The traverse permission applies only to directories'

    current_mode = adjust_bits(current_mode, stat.S_IRUSR, read)
    current_mode = adjust_bits(current_mode, stat.S_IWUSR, write)
    current_mode = adjust_bits(current_mode, stat.S_IXUSR, execute)
    current_mode = adjust_bits(current_mode, stat.S_IXUSR, traverse)

    chmod_fn = getattr(os, 'lchmod', os.chmod)
    chmod_fn(path, current_mode)


def check_file_rights(path, read=None, write=None, execute=None):
    return (
        ((read is None) or (os.access(path, os.R_OK) == read)) and
        ((write is None) or (os.access(path, os.W_OK) == write)) and
        ((execute is None) or (os.access(path, os.X_OK) == execute))
    )
