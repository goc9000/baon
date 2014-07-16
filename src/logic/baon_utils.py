# logic/baon_utils.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os
import string


from logic.str_utils import is_quoted_string


SIMPLE_ESCAPES = {
    'b':  '\b',
    't':  '\t',
    'n':  '\n',
    'f':  '\f',
    'r':  '\r',
    '"':  '"',
    "'":  "'",
    '\\': '\\'
}


def qstr_to_unicode(qstring):
    return unicode(qstring.toUtf8(), 'utf-8')


def decode_baon_string_literal(literal):
    if not is_quoted_string(literal):
        raise RuntimeError("{0} is not a valid string literal".format(literal))

    literal = literal[1:-1]  # strip quotes
    
    output_parts = []
    pos = 0
    
    while pos < len(literal):
        next_escape_pos = literal.find('\\', pos)
        if (next_escape_pos == -1) or (next_escape_pos == len(literal)-1):
            break
        
        output_parts.append(literal[pos:next_escape_pos])
        
        char_after_escape = literal[next_escape_pos+1]
        pos = next_escape_pos + 2
        
        if char_after_escape in SIMPLE_ESCAPES:  # simple escape
            output_parts.append(SIMPLE_ESCAPES[char_after_escape])
        elif char_after_escape == 'u' and pos < len(literal)-4 \
                and all(literal[pos+i] in string.hexdigits for i in xrange(4)):  # Unicode escape
            output_parts.append(unichr(int(literal[pos:pos+4], 16)))
            pos += 4
        elif char_after_escape in '01234567':  # octal escape
            code = int(char_after_escape)
            digits = 2 if code <= 3 else 1
            while (digits > 0) and (pos < len(literal)) and (literal[pos] in '01234567'):
                code = code * 8 + int(literal[pos])
                pos += 1
                digits -= 1
            
            output_parts.append(unichr(code))
        else:  # unsupported escape
            output_parts.append(u'\\')
            output_parts.append(char_after_escape)
    
    output_parts.append(literal[pos:])
    
    return u''.join(output_parts)


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
