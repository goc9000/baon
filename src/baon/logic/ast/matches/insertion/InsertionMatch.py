# baon/logic/ast/matches/insertion/InsertionMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.matches.MatchWithActions import MatchWithActions


class InsertionMatch(MatchWithActions):
    def __init__(self):
        MatchWithActions.__init__(self)