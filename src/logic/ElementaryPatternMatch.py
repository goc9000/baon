import re

from Match import Match
from RuleCheckException import RuleCheckException

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
        
    def semanticCheck(self, scope):
        if not self.error is None:
            raise RuleCheckException(self.error, scope)

        Match.semanticCheck(self, scope)