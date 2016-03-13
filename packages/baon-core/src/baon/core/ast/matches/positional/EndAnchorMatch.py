# baon/core/ast/matches/positional/EndAnchorMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.Match import Match


class EndAnchorMatch(Match):
    def __init__(self):
        Match.__init__(self)
    
    def execute(self, context):
        if context.position == len(context.text):
            yield context._replace(matched_text='', anchored=True)
