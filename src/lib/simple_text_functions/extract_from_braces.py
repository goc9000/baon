# lib/simple_text_functions/extract_from_braces.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


def inparas(text):
    return _extract_text_from_braces(text, u'(', u')', u'')


def inbraces(text):
    return _extract_text_from_braces(text, u'[', u']', u'')


def incurlies(text):
    return _extract_text_from_braces(text, u'{', u'}', u'')


def _extract_text_from_braces(text, left_brace, right_brace, fail_value=None):
    idx_from = text.find(left_brace)
    if idx_from == -1:
        return fail_value
    idx_from += len(left_brace)

    idx_to = text.find(right_brace, idx_from)
    if idx_to == -1:
        return fail_value

    return text[idx_from:idx_to]
