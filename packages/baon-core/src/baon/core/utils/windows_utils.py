# baon/core/windows_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os
import platform
import subprocess

from functools import lru_cache


def on_windows():
    return platform.system() == 'Windows'


@lru_cache()
def permissions_supported():
    try:
        subprocess.check_output('icacls /?')
    except:
        return False

    return True


def set_file_rights(path, read=None, write=None, execute=None, delete=None):
    is_dir = os.path.isdir(path)

    assert not is_dir or execute is None, 'The execute permission does not apply to directories'

    grant = []
    deny = []

    if read is not None:
        (grant if read else deny).append('RD')
    if write is not None:
        (grant if write else deny).extend(['WD', 'AD', 'DC'] if is_dir else ['WD', 'AD'])
    if execute is not None:
        (grant if execute else deny).append('X')
    if delete is not None:
        (grant if delete else deny).append('DE')

    username = get_username()

    params = ['icacls', path, '/l']

    if len(grant) > 0:
        params.extend(['/grant', '{0}:({1})'.format(username, ','.join(grant))])
    if len(deny) > 0:
        params.extend(['/deny', '{0}:({1})'.format(username, ','.join(deny))])

    subprocess.check_output(params)


def reset_file_rights(path, recursive=False):
    params = ['icacls', path, '/reset', '/l']
    if recursive:
        params.append('/t')

    subprocess.check_output(params)


@lru_cache()
def get_username():
    """
    Gets the effective username for use in operations involving access rights.

    This function is cached.
    """
    return subprocess.check_output('whoami').rstrip(b"\r\n").decode('UTF-8').rstrip("\r\n")
