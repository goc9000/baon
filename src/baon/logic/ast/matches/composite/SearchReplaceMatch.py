# baon/logic/ast/matches/composite/SearchReplaceMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.ASTNode import ast_node_child
from baon.logic.ast.matches.Match import Match
from baon.logic.ast.matches.composite.AlternativesMatch import AlternativesMatch
from baon.logic.ast.matches.composite.SequenceMatch import SequenceMatch
from baon.logic.ast.matches.composite.RepeatMatch import RepeatMatch
from baon.logic.ast.matches.special.BetweenMatch import BetweenMatch
from baon.logic.ast.matches.special.EndAnchorMatch import EndAnchorMatch


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

        solution = next(temp_match.execute(context), None)

        if solution is not None:
            yield context._replace(
                text=context.text[:context.position]+solution.matched_text,
                matched_text=u'',
            )
        else:
            yield context
