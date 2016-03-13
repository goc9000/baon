# baon/core/rules/MatchContext.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from collections import namedtuple


# Note: the reason we keep the entire (text, position) tuple instead of just the incoming text is so that we can
# correctly handle regexes with lookbehind assertions. This is also the reason why matched_text is a separate value
# (and we don't just replace the past portion of 'text')


MatchContext = namedtuple(
    'MatchContext',
    [
        'text',
        'position',
        'aliases',
        'matched_text',
        'anchored',
    ])
