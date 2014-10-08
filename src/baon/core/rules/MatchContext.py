# baon/core/rules/MatchContext.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from collections import namedtuple


MatchContext = namedtuple(
    'MatchContext',
    [
        'text',
        'position',
        'aliases',
        'matched_text',
        'anchored',
    ])
