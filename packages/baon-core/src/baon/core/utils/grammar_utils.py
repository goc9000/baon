# baon/core/grammar_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

# Note: I have not expended much effort in making these functions complete,
# correct in all situations, or portable to languages other than English. Beware.


import re

from collections import namedtuple


SimplePhrasePart = namedtuple('SimplePhrasePart', ['is_word', 'content', 'ws_before', 'ws_after'])


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


def format_count(item_count, item_name_singular, item_name_plural=None):
    if item_name_plural is None:
        item_name_plural = plural(item_name_singular)

    return "{0} {1}".format(item_count, item_name_singular if item_count == 1 else item_name_plural)


def format_tally(
        counts,
        names_singular,
        names_plural=None,
        omit_zero_entries=True,
        and_word=' and ',
        value_if_nothing='nothing',
        no_count_if_singleton=False,
):
    if names_plural is None:
        names_plural = [plural(name) for name in names_singular]
    if and_word is None:
        and_word = ', '

    assert len(counts) == len(names_singular) == len(names_plural)

    if sum(counts) == 1 and no_count_if_singleton:
        return next(name for item_count, name in zip(counts, names_singular) if item_count > 0)

    parts = [
        format_count(item_count, name_singular, name_plural)
        for item_count, name_singular, name_plural in zip(counts, names_singular, names_plural)
        if not (item_count == 0 and omit_zero_entries)
    ]

    if len(parts) == 0:
        return value_if_nothing
    elif len(parts) == 1:
        return parts[0]

    return ', '.join(parts[:-1]) + and_word + parts[-1]


def is_mac_name(word):
    return PAT_MAC_NAME.match(word) is not None


def is_compound_name(word):
    if len(word) == 0 or not word[0].isupper():
        return False

    any_dashes = False
    for i in range(1, len(word) - 1):
        if word[i] == '-':
            any_dashes = True
            if not word[i + 1].isupper():
                return False

    return any_dashes


def is_dash_char(c):
    return c in {'-', '\u2013', '\u2014'}


def is_particle(word):
    return word.lower() in PARTICLE_WORDS


def is_abbreviation(word):
    return word.lower() in {'vs'}


def capitalize_word(word, is_first_word=True, may_be_acronym=True):
    is_acronym = may_be_acronym and len(word) > 1 and word.isupper()

    if is_acronym or is_mac_name(word) or is_compound_name(word):
        return word

    if is_particle(word) and not is_first_word:
        return word.lower()

    return word.capitalize()


def to_title_case(phrase):
    phrase_is_upper = phrase.isupper()

    parts = find_words_and_separators(phrase, detect_abbreviations=True)
    if len(parts) == 0:
        return phrase

    for index, part in enumerate(parts):
        if not part.is_word:
            continue

        word = part.content

        is_acronym = word.isupper() and len(word) > 1 and not phrase_is_upper

        has_break_before = (index == 0) or (not parts[index-1].is_word and parts[index-1].content != ',')
        has_break_after = (index >= len(parts) - 1) or (not parts[index+1].is_word and parts[index+1].content != ',')

        if is_acronym or is_mac_name(word) or is_compound_name(word):
            pass  # leave unchanged
        elif is_particle(word) and not has_break_before and not has_break_after:
            word = word.lower()
        else:
            word = word.capitalize()

        parts[index] = parts[index]._replace(content=word)

    return parts[0].ws_before + ''.join([part.content + part.ws_after for part in parts])


def find_words_and_separators(phrase, detect_abbreviations=True):
    pat_alphanum = '[^\W_]'  # any Unicode alphanumeric except underscore

    pat_word_or_punctuation = '|'.join([
        "(?P<word>{0}((['-]|{0})*{0})?)".format(pat_alphanum),
        '(?P<fullstop_and_ellipsis>[.]+)',
        '(?P<q_and_e_marks>[!?]+)',
        "(?P<dashes>[\u2013\u2014-]+)",
        '(?P<other>\S)',
    ])

    matches = list(re.finditer(pat_word_or_punctuation, phrase, re.I + re.U))

    parts = []
    for index, match in enumerate(matches):
        prev_match_end = matches[index - 1].end() if index > 0 else 0
        next_match_start = matches[index + 1].start() if index < len(matches) - 1 else len(phrase)

        if detect_abbreviations:
            if match.group(0) == '.' and len(parts) > 0 and is_abbreviation(parts[-1].content) \
                    and parts[-1].ws_after == '':
                parts[-1] = parts[-1]._replace(
                    content=parts[-1].content + '.',
                    ws_after=phrase[match.end():next_match_start]
                )
                continue

        parts.append(SimplePhrasePart(
            is_word=match.group('word') is not None,
            content=match.group(0),
            ws_before=phrase[prev_match_end:match.start()],
            ws_after=phrase[match.end():next_match_start]
        ))

    return parts
