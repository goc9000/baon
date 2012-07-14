# logic/matches/LiteralMatch.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import re

from ElementaryPatternMatch import ElementaryPatternMatch

class LiteralMatch(ElementaryPatternMatch):
    def __init__(self, text):
        ElementaryPatternMatch.__init__(self)
        
        self._setPattern("({0})".format(re.escape(text)))
