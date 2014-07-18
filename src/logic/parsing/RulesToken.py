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
    lexpos = None
    lineno = None
    colno = None
    value = None

    def __getattribute__(self, item):
        if item == 'length':
            return len(self.text)
        elif item == 'start':
            return self.lexpos
        elif item == 'end':
            return self.lexpos + len(self.text)

        return object.__getattribute__(self, item)