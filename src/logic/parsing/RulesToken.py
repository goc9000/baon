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
    offset = None
    line = None
    column = None
    extra = None

    def length(self):
        return len(self.text)