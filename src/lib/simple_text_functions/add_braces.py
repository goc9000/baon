# lib/simple_text_functions/add_braces.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


def paras(text):
    return _add_braces(text, u'(', u')')


def braces(text):
    return _add_braces(text, u'[', u']')


def curlies(text):
    return _add_braces(text, u'{', u'}')


def _add_braces(text, left_brace, right_brace):
    mid_text = text.lstrip()
    left_space = text[0:len(text) - len(mid_text)]
    mid_text = mid_text.rstrip()
    right_space = text[len(left_space) + len(mid_text):]

    return left_space + left_brace + mid_text + right_brace + right_space
