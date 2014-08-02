# logic/ast/rules/RuleSet.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.ASTNode import ASTNode, ast_node_children

from logic.rules.MatchContext import MatchContext


class RuleSet(ASTNode):
    rules = ast_node_children()
    
    def __init__(self):
        ASTNode.__init__(self)
        self.rules = []

    def apply_on(self, text, initial_aliases=None):
        aliases = initial_aliases.copy() if initial_aliases is not None else dict()

        for rule in self.rules:
            context = MatchContext(text, aliases)
            matched = rule.execute(context)

            if matched is not False and context.aliases != aliases:
                context = MatchContext(text, context.aliases)
                matched = rule.execute(context)
            
            if matched is not False:
                text = matched + context.text[context.position:]
                aliases = dict(context.aliases)

        return text, aliases

    def is_empty(self):
        return len(self.rules) == 0
