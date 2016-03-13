# baon/core/ast/matches/material/MaterialMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import abstractmethod

from baon.core.ast.matches.Match import Match


class MaterialMatch(Match):
    """
    Material matches are those that depend on the content of and position in the input text.

    After the execution of a material match, the 'anchored' context field is guaranteed to be true. This is significant
    in the functioning of the Between match, which essentially will extend to the next anchored match.
    """
    def __init__(self):
        Match.__init__(self)

    def execute(self, context):
        for solution in self._execute_material_match_impl(context):
            yield solution._replace(anchored=True)

    @abstractmethod
    def _execute_material_match_impl(self, context):
        return []
