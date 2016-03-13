# baon/core/ast/matches/material/positional/EndAnchorMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.matches.material.MaterialMatch import MaterialMatch


class EndAnchorMatch(MaterialMatch):
    def __init__(self):
        MaterialMatch.__init__(self)
    
    def _execute_material_match_impl(self, context):
        if context.position == len(context.text):
            yield context._replace(matched_text='')
