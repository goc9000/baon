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
PAT_MAC_NAME = re.compile(r"Ma?c[A-Z]")

PARTICLE_WORDS = {'a', 'an', 'and', 'as', 'at', 'by', 'but', 'of', 'with', 'for', 'in', 'on', 'to', 'the', 'vs'}

PARA_CHARS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '"': '"',
    "'": "'"
}


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


def is_mac_name(word):
    return PAT_MAC_NAME.match(word) is not None


def is_particle(word):
    return word.lower() in PARTICLE_WORDS


def capitalize_word(word, is_first_word=True, may_be_acronym=True):
    is_acronym = may_be_acronym and len(word) > 1 and word.isupper()

    if is_acronym or is_mac_name(word):
        return word

    if is_particle(word) and not is_first_word:
        return word.lower()

    return word.capitalize()


def to_title_case(phrase):
    phrase_is_upper = phrase.isupper()

    is_first_word_stack = [True]
    expected_rpara_stack = ['']

    parts = list(enum_words_and_sep(phrase))

    for i in xrange(1, len(parts), 2):
        for c in parts[i - 1]:
            if c == expected_rpara_stack[-1]:
                expected_rpara_stack.pop()
                is_first_word_stack.pop()
            elif c in PARA_CHARS:
                is_first_word_stack.append(True)
                expected_rpara_stack.append(PARA_CHARS[c])

        # Kludge to catch cases like "Name A. Surname"
        is_initial = parts[i] == 'A' and parts[i + 1].startswith('.')

        if not is_initial:
            parts[i] = capitalize_word(parts[i],
                                       is_first_word=is_first_word_stack[-1],
                                       may_be_acronym=not phrase_is_upper)

        is_first_word_stack[-1] = False

    return ''.join(parts)


def enum_words_and_sep(phrase):
    pos = 0
    while pos < len(phrase):
        m = PAT_WORD.search(phrase, pos)
        if m is None:
            break
    
        yield phrase[pos:m.start()]
        yield m.group(0)
        pos = m.end()
        
    yield phrase[pos:]


def aesthetic_warning(phrase):
    if phrase.startswith(' '):
        return 'starts with spaces'
    if phrase.endswith(' '):
        return 'ends with spaces'
    if '  ' in phrase:
        return 'contains double spaces'
    
    return None
