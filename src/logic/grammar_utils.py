# logic/grammar_utils.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

# Note: I have not expended much effort in making these functions complete,
# correct in all situations, or portable to languages other than English. Beware.

import re

PAT_WORD = re.compile(r"[^\W_]((['-]|[^\W_])*[^\W_])?", re.I | re.U)

PARTICLE_WORDS = {'a', 'an', 'and', 'as', 'at', 'by', 'but', 'of', 'with', 'for', 'in', 'on', 'to', 'the', 'vs'}


def plural(word):
    # Incomplete and buggy, of course; word must be lowercase
    if len(word) == 1:
        return word + "'s"
    if word[-1] == 'y' and word[-2] not in {'a', 'e', 'i', 'o', 'u'}:
        return word[:-1] + "ies"
    if word[-2:] in ('sh', 'ch'):
        return word + "es"
    
    return word + "s"


def format_numeral(item_name_singular, item_count):
    name = item_name_singular if item_count == 1 else plural(item_name_singular)
    
    return "{0} {1}".format(item_count, name)


def format_numerals(counts, omit_zero_entries=True, value_if_nothing='nothing'):
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


def is_particle(word):
    return word.lower() in PARTICLE_WORDS


def to_title_case(phrase):
    out = []
    
    first = True
    
    phrase_is_upper = phrase.isupper()

    for text, is_word in enum_words_and_sep(phrase):
        if is_word:
            is_acronym = len(text) > 1 and text.isupper() and not phrase_is_upper
            
            if is_acronym:
                out.append(text)
            elif is_particle(text) and not first:
                out.append(text.lower())
            else:
                out.append(text.capitalize())
            
            first = False
        else:
            out.append(text)
    
    return ''.join(out)


def enum_words_and_sep(phrase):
    pos = 0
    while pos < len(phrase):
        m = PAT_WORD.search(phrase, pos)
        if m is None:
            break
    
        if m.start() != pos:
            yield (phrase[pos:m.start()], False)
        
        yield (m.group(0), True)
        pos = m.end()
        
    if pos != len(phrase):
        yield (phrase[pos:], False)


def aesthetic_warning(phrase):
    if phrase.startswith(' '):
        return 'starts with spaces'
    if phrase.endswith(' '):
        return 'ends with spaces'
    if '  ' in phrase:
        return 'contains double spaces'
    
    return None
