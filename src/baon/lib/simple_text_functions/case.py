# baon/lib/simple_text_functions/case.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.grammar_utils import to_title_case


def title(text):
    return to_title_case(text)


def upper(text):
    return text.upper()


def toupper(text):
    return text.upper()


def lower(text):
    return text.lower()


def tolower(text):
    return text.lower()
