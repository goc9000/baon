# logic/ast/rules/Rule.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from logic.ast.ASTNode import ASTNode, ast_node_child

from logic.errors.RuleApplicationException import RuleApplicationException

from logic.rules.MatchContext import MatchContext
from logic.rules.ApplyRuleResult import ApplyRuleResult


MAX_ITERATIONS = 10


class Rule(ASTNode):
    content = ast_node_child()
    
    def __init__(self, content):
        ASTNode.__init__(self)
        self.content = content

    def is_empty(self):
        return self.content.is_empty()

    def apply_on(self, text, aliases=None):
        initial_aliases = dict(aliases) if aliases is not None else dict()

        aliases = initial_aliases

        for _ in xrange(MAX_ITERATIONS):
            context = MatchContext(text, aliases)
            matched = self.content.execute(context)

            if context.aliases != aliases:
                aliases = dict(context.aliases)
                continue

            if matched is not False:
                text = matched + context.text[context.position:]

            return ApplyRuleResult(text=text, aliases=aliases)

        raise RuleApplicationException("Dependencies of aliases are too complex")
