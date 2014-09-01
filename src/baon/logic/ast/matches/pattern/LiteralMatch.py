# baon/logic/ast/matches/pattern/LiteralMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import re

from baon.logic.ast.matches.pattern.ElementaryPatternMatch import ElementaryPatternMatch

from baon.logic.ast.ASTNode import ast_node_field


class LiteralMatch(ElementaryPatternMatch):
    text = ast_node_field()

    def __init__(self, text):
        ElementaryPatternMatch.__init__(self)

        self.text = text

    def _get_pattern_impl(self):
        return re.escape(self.text)
