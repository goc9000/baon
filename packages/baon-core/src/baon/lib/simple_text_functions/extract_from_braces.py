# baon/lib/simple_text_functions/extract_from_braces.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import re


def inparens(text):
    return _extract_text_from_braces(text, '(', ')', '')


def inbraces(text):
    return _extract_text_from_braces(text, '[', ']', '')


def incurlies(text):
    return _extract_text_from_braces(text, '{', '}', '')


def _extract_text_from_braces(text, left_brace, right_brace, fail_value=None):
    pattern = re.escape(left_brace) + '([^' + re.escape(left_brace + right_brace) + ']+)' + re.escape(right_brace)

    match = re.search(pattern, text)

    return match.group(1) if match is not None else fail_value
