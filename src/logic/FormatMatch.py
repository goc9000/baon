import re

from ElementaryPatternMatch import ElementaryPatternMatch

class FormatMatch(ElementaryPatternMatch):
    fmt_spec_error = None
    
    def __init__(self, fmt_spec):
        ElementaryPatternMatch.__init__(self)
        
        pattern = self._makePattern(fmt_spec)

        if pattern is not None:
            self._setPattern(pattern)
        else:
            self._setError("Unrecognized format specifier '{0}'".format(fmt_spec))

    def _makePattern(self, fmt_spec):
        if fmt_spec == '%ws':
            return r'(\s*)'
        
        m = re.match(r'%([0-9]*)d', fmt_spec)
        if m is not None:
            return r'(\s*[0-9]+)' if len(m.group(1)) == 0 else r'(\s*[0-9]{{{0}}})'.format(int(m.group(1)))

        m = re.match(r'%([0-9]*)c', fmt_spec)
        if m is not None:
            return r'(.)' if len(m.group(1)) == 0 else r'(.{{{0}}})'.format(int(m.group(1)))

        m = re.match(r'%([0-9]*)s', fmt_spec)
        if m is not None:
            return r'(\s*\S+)' if len(m.group(1)) == 0 else r'(\s*\S{{{0}}})'.format(int(m.group(1)))
        
        return None
