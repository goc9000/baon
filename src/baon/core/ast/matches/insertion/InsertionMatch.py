# baon/core/ast/matches/insertion/InsertionMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import abstractmethod

from baon.core.ast.matches.MatchWithActions import MatchWithActions


class InsertionMatch(MatchWithActions):
    def __init__(self):
        MatchWithActions.__init__(self)

    def _execute_match_with_actions_impl(self, context):
        yield context._replace(matched_text=self._get_inserted_text_impl(context))

    @abstractmethod
    def _get_inserted_text_impl(self, context):
        return ''
