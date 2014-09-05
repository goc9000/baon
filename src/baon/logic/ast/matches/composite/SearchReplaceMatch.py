# baon/logic/ast/matches/composite/SearchReplaceMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.logic.ast.ASTNode import ast_node_child
from baon.logic.ast.matches.Match import Match

from baon.logic.rules.MatchContextOld import MatchContextOld


class SearchReplaceMatch(Match):
    term = ast_node_child()
    
    def __init__(self, term):
        Match.__init__(self)
        self.term = term

    def execute(self, context):
        ctx = MatchContextOld(context.text, context.aliases)
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