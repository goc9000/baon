import os

def decode_literal(literal):
    return literal[1:-1].decode("unicode_escape")

def enum_partial_paths(path):
    """
    Enumerates all non-empty parents of the given relative path, from the
    shortest to the longest.
    
    Does not work on absolute paths.
    """
    path, _ = os.path.split(path)
    
    base = ''
    
    if path != '':
        for comp in path.split(os.sep):
            base = os.path.join(base, comp)
            yield base
