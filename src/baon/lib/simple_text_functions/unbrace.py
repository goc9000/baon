# baon/lib/simple_text_functions/unbrace.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import re


PAT_BRACE = re.compile(r"[()\[\]{}]")


def unbrace(text):
    return PAT_BRACE.sub(u'', text)
