# baon/core/ast/matches/special/BetweenMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.Match import Match


class BetweenMatch(Match):
    def __init__(self):
        Match.__init__(self)

    def execute(self, context):
        if context.anchored:
            for end in range(context.position, len(context.text) + 1):
                yield context._replace(
                    position=end,
                    matched_text=context.text[context.position:end],
                    anchored=False,
                )
        else:
            yield context._replace(matched_text='')
