# baon/core/ast/rules/Rule.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.ast.ASTNode import ASTNode, ast_node_child

from baon.core.errors.RuleApplicationException import RuleApplicationException

from baon.core.ast.matches.control.SequenceMatch import SequenceMatch
from baon.core.ast.matches.positional.EndAnchorMatch import EndAnchorMatch
from baon.core.ast.matches.special.BetweenMatch import BetweenMatch

from baon.core.rules.MatchContext import MatchContext
from baon.core.rules.ApplyRuleResult import ApplyRuleResult


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

        temp_match = SequenceMatch(
            self.content,
            BetweenMatch(),
            EndAnchorMatch(),
        )
        initial_context = MatchContext(
            text=text,
            position=0,
            aliases=initial_aliases,
            matched_text=None,
            anchored=True,
        )

        for _ in xrange(MAX_ITERATIONS):
            solution = next(temp_match.execute(initial_context), None)
            if solution is None:
                return ApplyRuleResult(text=text, aliases=initial_aliases)

            if solution.aliases != initial_context.aliases:
                initial_context = initial_context._replace(aliases=solution.aliases)
                continue

            return ApplyRuleResult(text=solution.matched_text, aliases=solution.aliases)

        raise RuleApplicationException("Dependencies of aliases are too complex")
