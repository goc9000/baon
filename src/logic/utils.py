# logic/utils.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import os, string

ESCAPES = {
    'b'  : '\b',
    't'  : '\t',
    'n'  : '\n',
    'f'  : '\f',
    'r'  : '\r',
    '"'  : '"',
    "'"  : "'",
    '\\' : '\\'
}

def qstr_to_unicode(qstring):
    return unicode(qstring.toUtf8(), 'utf-8')

def decode_literal(literal):
    literal = literal[1:-1]
    
    out = []
    pos = 0
    
    while pos < len(literal):
        nxpos = literal.find('\\', pos)
        if (nxpos == -1) or (nxpos == len(literal)-1):
            break
        
        out.append(literal[pos:nxpos])
        
        esc_char = literal[nxpos+1]
        pos = nxpos + 2
        
        if esc_char in ESCAPES: # simple escape
            out.append(ESCAPES[esc_char])
        elif esc_char == 'u' and pos < len(literal)-4 \
            and all(literal[pos+i] in string.hexdigits for i in xrange(4)): # Unicode escape
            out.append(unichr(int(literal[pos:pos+4], 16)))
            pos += 4
        elif esc_char in '01234567': # octal escape
            code = int(esc_char)
            digits = 2 if code <= 3 else 1
            while (digits > 0) and (pos < len(literal)) and (literal[pos] in '01234567'):
                code = code*8 + int(literal[pos])
                pos += 1
                digits -= 1
            
            out.append(chr(code))
        else: # unsupported escape
            out.append(esc_char)
    
    out.append(literal[pos:])
    
    return ''.join(out)

def enum_partial_paths(path):
    """
    Enumerates all non-empty parents of the given relative path, from the shortest to the longest.
    
    Does not work on absolute paths.
    """
    path, _ = os.path.split(path)
    
    base = ''
    
    if path != '':
        for comp in path.split(os.sep):
            base = os.path.join(base, comp)
            yield base
