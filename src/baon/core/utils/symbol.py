# baon/core/symbol.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


def symbol(name):
    if name not in _symbols:
        _symbols[name] = _Symbol(name)

    return _symbols[name]


_symbols = {}


class _Symbol:
    _name = None

    def __init__(self, name):
        self._name = name

    def __str__(self):
        return '<sym:{0}>'.format(self._name)
