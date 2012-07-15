# logic/matches/FormatMatch.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import os, re

from ElementaryPatternMatch import ElementaryPatternMatch

FORMAT_DICT = {
    '%ws'        : r'(\s*)',
    '%d'         : r'(\s*[0-9]+)',
    '%c'         : r'(.)',
    '%s'         : r'(\s*\S+)',
    '%paras'     : r'(\s*\([^)]*\))',
    '%inparas'   : r'((?<=\()[^)]*(?=\)))',
    '%braces'    : r'(\s*\[[^\]]*\])',
    '%inbraces'  : r'((?<=\[[^\]]*(?=\]))',
    '%curlies'   : r'(\s*\{[^}]*\})',
    '%incurlies' : r'((?<=\{[^}]*(?=\}))',
    '%path'      : r'(.*' + re.escape(os.sep) + r')'
}

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
        if fmt_spec in FORMAT_DICT:
            return FORMAT_DICT[fmt_spec]
        
        m = re.match(r'%([0-9]+)d$', fmt_spec)
        if m is not None: return r'(\s*[0-9]{{{0}}})'.format(int(m.group(1)))

        m = re.match(r'%([0-9]+)c$', fmt_spec)
        if m is not None: return r'(.{{{0}}})'.format(int(m.group(1)))

        m = re.match(r'%([0-9]+)s$', fmt_spec)
        if m is not None: return r'(\s*\S{{{0}}})'.format(int(m.group(1)))
        
        return None
