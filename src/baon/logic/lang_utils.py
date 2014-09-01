# baon/logic/lang_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import sys


def is_python3():
    return sys.version_info[0] >= 3


def is_string(x):
    if is_python3():
        str_base_type = str
    else:
        str_base_type = basestring

    return isinstance(x, str_base_type)


def is_arrayish(x):
    """Checks whether x is arrayish, i.e. a collection capable of random access by 0-based numerical index."""
    return hasattr(x, '__getslice__') and not is_string(x)


def is_dictish(x):
    """Checks whether x is dictish, i.e. a dict-like object accessible by any key."""
    return hasattr(x, '__getitem__') and not hasattr(x, '__getslice__') and not is_string(x)
