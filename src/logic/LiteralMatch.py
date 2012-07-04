import re

from ElementaryPatternMatch import ElementaryPatternMatch

class LiteralMatch(ElementaryPatternMatch):
    def __init__(self, text):
        ElementaryPatternMatch.__init__(self)
        
        self._setPattern("({0})".format(re.escape(text)))
