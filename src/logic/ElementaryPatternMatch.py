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

    def execute(self, context):
        m = self.regex.match(context.text, context.position)

        if m == None:
            return False

        result = self.runActions(m.group(1), context)
        if result is False:
            return False

        context.position += len(m.group(0))

        return result
