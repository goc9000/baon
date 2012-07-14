# logic/matches/ElementaryPatternMatch.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import re

from Match import Match
from logic.errors.RuleCheckException import RuleCheckException

class ElementaryPatternMatch(Match):
    regex = None
    error = None

    def __init__(self):
        Match.__init__(self)

    def _setPattern(self, pattern, flags=0):
        try:
            self.regex = re.compile(pattern, flags)
        except:
            self._setError("Regex /{0}/ is not valid".format(pattern));

    def _setError(self, message):
        self.error = message
        
    def _semanticCheck(self, scope):
        if not self.error is None:
            raise RuleCheckException(self.error, scope)

    def _execute(self, context):
        if context.next_unanchored:
            m = self.regex.search(context.text, context.position)
            context.next_unanchored = False
        else:
            m = self.regex.match(context.text, context.position)

        if m is None:
            return False

        context.position = m.end(0)
        context.last_match_pos = m.start(1)

        return m.group(1)
