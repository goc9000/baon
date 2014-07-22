# logic/ast/matches/composite/MatchSequence.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.RulesASTNode import RulesASTNode

from logic.ast.matches.special.BetweenMatch import BetweenMatch


class MatchSequence(RulesASTNode):
    terms = None

    def __init__(self):
        RulesASTNode.__init__(self)
        self.terms = []

    def is_empty(self):
        return len(self.terms) == 0

    def semanticCheck(self, scope):
        for term in self.terms:
            term.semanticCheck(scope)

    def execute(self, context):
        savept = context.save()
        committed = []
        
        match_pos = None
        pending_betw_match_idx = None
        pending_betw_match_pos = None

        for idx in xrange(len(self.terms)):
            term = self.terms[idx]
            matched = term.execute(context)

            if matched is False:
                context.restore(savept)
                return False
            
            if context.last_match_pos is not None:
                if pending_betw_match_idx is not None:
                    late_match = self.terms[pending_betw_match_idx].executeDelayed(
                        context.text[pending_betw_match_pos:context.last_match_pos],
                        context)
                    if late_match is False:
                        context.restore(savept)
                        return False
                    committed[pending_betw_match_idx] = late_match
                    pending_betw_match_idx = None
                
                if match_pos is None:
                    match_pos = context.last_match_pos

            if isinstance(term, BetweenMatch):
                pending_betw_match_idx = idx
                pending_betw_match_pos = context.position

            committed.append(matched)

        if pending_betw_match_idx is not None:
            # ".."s at the end will match all remaining text
            late_match = self.terms[pending_betw_match_idx].executeDelayed(
                context.text[pending_betw_match_pos:len(context.text)],
                context)
            if late_match is False:
                context.restore(savept)
                return False
            context.position = len(context.text)
            committed[pending_betw_match_idx] = late_match

        context.last_match_pos = match_pos

        return ''.join(committed)

    def _test_repr_children(self):
        return self.terms
