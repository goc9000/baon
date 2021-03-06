# baon/core/ast/matches/immaterial/insertion/InsertAliasMatch.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.ASTNode import ast_node_field
from baon.core.ast.matches.immaterial.insertion.InsertionMatch import InsertionMatch


class InsertAliasMatch(InsertionMatch):
    alias = ast_node_field()
    
    def __init__(self, alias):
        InsertionMatch.__init__(self)

        self.alias = alias

    def _get_inserted_text_impl(self, context):
        return context.aliases.get(self.alias, '')
