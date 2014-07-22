# logic/matches/special/SearchReplaceMatch.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.parsing.RulesASTNode import RulesASTNode

from logic.matches.MatchContext import MatchContext


class SearchReplaceMatch(RulesASTNode):
    term = None
    
    def __init__(self, term):
        RulesASTNode.__init__(self)
        self.term = term
    
    def semanticCheck(self, scope):
        self.term.semanticCheck(scope)

    def execute(self, context):
        ctx = MatchContext(context.text, context.aliases)
        ctx.position = context.position
        
        new_text = []
        while ctx.position <= len(ctx.text):
            prev_pos = ctx.position
            ctx.next_unanchored = True
            ctx.last_match_pos = None
            matched = self.term.execute(ctx)
            if matched is False:
                break
            
            if ctx.last_match_pos is not None:
                new_text.append(ctx.text[prev_pos:ctx.last_match_pos])
            new_text.append(matched)
            
            if ctx.last_match_pos is None:
                break
            
            if ctx.position == prev_pos:
                ctx.position += 1
        
        if ctx.position < len(ctx.text):
            new_text.append(ctx.text[ctx.position:])
        
        context.text = context.text[:context.position] + ''.join(new_text)
        
        return ''

    def test_repr(self):
        return 'SEARCH_MATCH', self.term.test_repr()
