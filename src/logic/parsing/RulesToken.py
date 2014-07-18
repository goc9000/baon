# logic/parsing/RulesToken.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


class RulesToken(object):
    type = None
    text = None
    start = None
    line = None
    column = None
    extra = None

    def __getattribute__(self, item):
        if item == 'length':
            return len(self.text)
        elif item == 'end':
            return self.start + len(self.text)

        return object.__getattribute__(self, item)