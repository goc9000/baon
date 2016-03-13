# baon/core/ast/matches/insertion/InsertionMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import abstractmethod

from baon.core.ast.matches.Match import Match


class InsertionMatch(Match):
    def __init__(self):
        Match.__init__(self)

    def execute(self, context):
        yield context._replace(matched_text=self._get_inserted_text_impl(context))

    @abstractmethod
    def _get_inserted_text_impl(self, context):
        return ''
