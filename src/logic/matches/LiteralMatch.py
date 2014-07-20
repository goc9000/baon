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
    _original_text = None

    def __init__(self, text):
        ElementaryPatternMatch.__init__(self)
        
        self._setPattern("({0})".format(re.escape(text)))
        self._original_text = text

    def _test_repr_impl(self):
        return 'LITERAL_MATCH', self._original_text
