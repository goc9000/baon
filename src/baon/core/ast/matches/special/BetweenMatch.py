# baon/core/ast/matches/special/BetweenMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.MatchWithActions import MatchWithActions


class BetweenMatch(MatchWithActions):
    def __init__(self):
        MatchWithActions.__init__(self)

    def _execute_match_with_actions_impl(self, context):
        if context.anchored:
            for end in xrange(context.position, len(context.text) + 1):
                yield context._replace(
                    position=end,
                    matched_text=context.text[context.position:end],
                    anchored=False,
                )
        else:
            yield context._replace(matched_text=u'')
