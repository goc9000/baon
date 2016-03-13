# baon/core/ast/matches/immaterial/insertion/InsertionMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import abstractmethod

from baon.core.ast.matches.immaterial.ImmaterialMatch import ImmaterialMatch


class InsertionMatch(ImmaterialMatch):
    def __init__(self):
        ImmaterialMatch.__init__(self)

    def _execute_immaterial_match_impl(self, context):
        yield context._replace(matched_text=self._get_inserted_text_impl(context))

    @abstractmethod
    def _get_inserted_text_impl(self, context):
        return ''
