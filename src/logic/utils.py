import os

def decode_literal(literal):
    return literal[1:-1].decode("unicode_escape")

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
