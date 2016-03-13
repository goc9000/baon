# baon/core/ast/matches/immaterial/ImmaterialMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import abstractmethod

from baon.core.ast.matches.Match import Match


class ImmaterialMatch(Match):
    """
    Immaterial matches are those that do not depend on the incoming text for succeeding. They will always "match",
    consume no text input, and do not change the anchoring status.
    """
    def __init__(self):
        Match.__init__(self)

    def execute(self, context):
        for solution in self._execute_immaterial_match_impl(context):
            assert solution.position == context.position
            assert solution.anchored == context.anchored

            yield solution

    @abstractmethod
    def _execute_immaterial_match_impl(self, context):
        return []
