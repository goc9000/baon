# logic/ast/matches/insertion/InsertionMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.matches.Match import Match


class InsertionMatch(Match):
    def __init__(self):
        Match.__init__(self)