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

def plural(word):
    # Incomplete and buggy, of course; word must be lowercase
    if len(word) == 1:
        return word + "'s"
    if word[-1] == 'y' and word[-2] not in ('a','e','i','o','u'):
        return word[:-1] + "ies"
    if word[-2:] in ('sh', 'ch'):
        return word + "es"
    
    return word + "s"    

def format_numeral(item_name_singular, item_count):
    name = item_name_singular if item_count == 1 else plural(item_name_singular)
    
    return "{0} {1}".format(item_count, name)

def format_numerals(counts, omit_zero_entries = True, value_if_nothing='nothing'):
    parts = []
    
    if omit_zero_entries:
        counts = [item for item in counts if item[1] > 0]
    
    for i, item in enumerate(counts):
        if i > 0:
            parts.append(', ' if i != len(counts)-1 else ' and ')
        
        parts.append(format_numeral(item[0], item[1]))
    
    if len(parts) == 0:
        return value_if_nothing
    
    return ''.join(parts)
