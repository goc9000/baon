# baon/core/lang_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import sys

from collections import deque
from itertools import tee, zip_longest
from inspect import isabstract
from contextlib import contextmanager


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
    return hasattr(x, '__getitem__') and not hasattr(x, 'keys') and not is_string(x)


def is_dictish(x):
    """Checks whether x is dictish, i.e. a dict-like object accessible by any key."""
    return hasattr(x, '__getitem__') and hasattr(x, 'keys') and not is_string(x)


def is_callable(x):
    return hasattr(x, '__call__')


@contextmanager
def swallow_os_errors():
    try:
        yield
    except OSError:
        pass


@contextmanager
def swallow_all_errors():
    try:
        yield
    except:
        pass


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def chunked(iterable, n, fill_value=None):
    """chunked('ABCDEFG', 3, 'x') -> ABC DEF Gxx"""
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fill_value)


def iter_non_abstract_descendants(cls):
    q = deque()
    q.append(cls)

    while len(q) > 0:
        cls = q.popleft()
        q.extend(cls.__subclasses__())

        if not isabstract(cls):
            yield cls
