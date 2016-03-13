# baon/core/ast/matches/special/SearchReplaceMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.ASTNode import ast_node_child
from baon.core.ast.matches.Match import Match
from baon.core.ast.matches.composite.AlternativesMatch import AlternativesMatch
from baon.core.ast.matches.composite.RepeatMatch import RepeatMatch
from baon.core.ast.matches.composite.SequenceMatch import SequenceMatch
from baon.core.ast.matches.material.positional.EndAnchorMatch import EndAnchorMatch
from baon.core.ast.matches.special.BetweenMatch import BetweenMatch


class SearchReplaceMatch(Match):
    term = ast_node_child()
    
    def __init__(self, term):
        Match.__init__(self)
        self.term = term

    def execute(self, context):
        temp_match = SequenceMatch(
            RepeatMatch(
                AlternativesMatch(
                    self.term,
                    BetweenMatch(),
                ),
                0,
                None,
            ),
            BetweenMatch(),
            EndAnchorMatch(),
        )
        temp_context = context._replace(anchored=True)

        solution = next(temp_match.execute(temp_context), None)

        if solution is not None:
            yield context._replace(
                text=context.text[:context.position]+solution.matched_text,
                matched_text='',
                aliases=solution.aliases,
            )
        else:
            yield context._replace(matched_text='')
