import re

from ElementaryPatternMatch import ElementaryPatternMatch

class RegexMatch(ElementaryPatternMatch):
    def __init__(self, patt_text):
        ElementaryPatternMatch.__init__(self)

        delim_chr = patt_text[0]
        patt_text = patt_text.replace(delim_chr*2, delim_chr)
        idx = patt_text.rfind(delim_chr)
        flags = 0

        for c in patt_text[idx+1:]:
            if c == 'i':
                flags |= re.I;
            else:
                self._setError("Invalid regex flag '{0}'".format(c))
                return

        self._setPattern("({0})".format(patt_text[1:idx]), flags)
