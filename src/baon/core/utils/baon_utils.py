# baon/core/baon_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import string

from baon.core.utils.str_utils import is_quoted_string
from baon.core.parsing.rule_parse_exceptions import StringLiteralNotQuotedProperlyException


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


def decode_baon_string_literal(literal):
    if not is_quoted_string(literal):
        raise StringLiteralNotQuotedProperlyException()

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
        elif char_after_escape == 'u' and pos <= len(literal)-4 \
                and all(literal[pos+i] in string.hexdigits for i in range(4)):  # Unicode escape
            output_parts.append(chr(int(literal[pos:pos+4], 16)))
            pos += 4
        elif char_after_escape in '01234567':  # octal escape
            code = int(char_after_escape)
            digits = 2 if code <= 3 else 1
            while (digits > 0) and (pos < len(literal)) and (literal[pos] in '01234567'):
                code = code * 8 + int(literal[pos])
                pos += 1
                digits -= 1
            
            output_parts.append(chr(code))
        else:  # unsupported escape
            output_parts.append('\\')
            output_parts.append(char_after_escape)

    output_parts.append(literal[pos:])

    return ''.join(output_parts)
