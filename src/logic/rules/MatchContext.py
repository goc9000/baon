# logic/rules/MatchContext.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


class MatchContext(object):
    text = None
    position = None
    stop = None
    aliases = None
    forward_aliases = None
    next_unanchored = None
    last_match_pos = None
    
    def __init__(self, text, initial_aliases=None):
        self.text = text
        self.position = 0
        self.stop = False
        self.forward_aliases = set()
        self.aliases = initial_aliases.copy() if not initial_aliases is None else dict()
        self.next_unanchored = False
        self.last_match_pos = None

    def save(self):
        # Note: last_match_pos is not saved; it is a secondary output parameter meant to be used immediately
        return (self.text,
                self.position,
                self.stop,
                self.forward_aliases.copy(),
                self.aliases.copy(),
                self.next_unanchored)

    def restore(self, savepoint):
        self.text = savepoint[0]
        self.position = savepoint[1]
        self.stop = savepoint[2]
        self.forward_aliases = savepoint[3].copy()
        self.aliases = savepoint[4].copy()
        self.next_unanchored = savepoint[5]
