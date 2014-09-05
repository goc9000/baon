# baon/lib/simple_text_functions/extract_from_braces.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import re


def inparas(text):
    return _extract_text_from_braces(text, u'(', u')', u'')


def inbraces(text):
    return _extract_text_from_braces(text, u'[', u']', u'')


def incurlies(text):
    return _extract_text_from_braces(text, u'{', u'}', u'')


def _extract_text_from_braces(text, left_brace, right_brace, fail_value=None):
    pattern = re.escape(left_brace) + u'([^' + re.escape(left_brace + right_brace) + u']+)' + re.escape(right_brace)

    match = re.search(pattern, text)

    return match.group(1) if match is not None else fail_value
