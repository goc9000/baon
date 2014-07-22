# logic/matches/pattern/LiteralMatch.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import re

from ElementaryPatternMatch import ElementaryPatternMatch


class LiteralMatch(ElementaryPatternMatch):
    text = None

    def __init__(self, text):
        ElementaryPatternMatch.__init__(self)

        self.text = text

    def _get_pattern_impl(self):
        return re.escape(self.text)

    def _test_repr_node_name(self):
        return 'LITERAL_MATCH'

    def _test_repr_params(self):
        return self.text,
