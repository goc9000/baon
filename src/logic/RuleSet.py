class RuleSet(object):
    rules = None
    
    def __init__(self):
        self.rules = []

    def isEmpty(self):
        return len(self.rules) == 0
    
    def semanticCheck(self, scope=None):
        if scope is None:
            scope = SemCheckScope()
        
        scope.EnterRuleSet(self)
        for rule in self.rules:
            rule.semanticCheck(scope)
        scope.ExitRuleSet()

    
class Rule(object):
    terms = None
    
    def __init__(self):
        self.terms = []

    def semanticCheck(self, scope):
        scope.EnterRule(self)
        for term in self.terms:
            term.semanticCheck(scope)
        scope.ExitRule()


class Term(object):
    match = None
    actions = None
    
    def __init__(self):
        self.actions = []

    def semanticCheck(self, scope):
        scope.EnterTerm(self)
        self.match.semanticCheck(scope)
        for action in self.actions:
            action.semanticCheck(scope)
        scope.ExitTerm()


class Match(object):
    def __init__(self):
        pass
    
    def semanticCheck(self, scope):
        pass


class LiteralMatch(Match):
    literalText = None
    
    def __init__(self, literalText):
        Match.__init__(self)
        
        self.literalText = literalText

        
class BetweenMatch(Match):
    def __init(self):
        Match.__init__(self)

    def semanticCheck(self, scope):
        index = scope.GetTermIndex()
        if index > 0:
            if isinstance(scope.rule.terms[index-1].match, BetweenMatch):
                raise RuleCheckException("Consecutive '..' matches not allowed", scope)


class InsertionMatch(Match):
    def __init__(self):
        Match.__init__(self)


class InsertLiteralMatch(InsertionMatch):
    literalText = None
    
    def __init__(self, literalText):
        InsertionMatch.__init__(self)
        
        self.literalText = literalText


class InsertAliasMatch(InsertionMatch):
    alias = None
    
    def __init__(self, alias):
        InsertionMatch.__init__(self)
        
        self.alias = alias


class Action(object):
    def __init__(self):
        pass

    def semanticCheck(self, scope):
        pass


class DeleteAction(Action):
    def __init__(self):
        Action.__init__(self)


class SaveAction(Action):
    alias = None
    
    def __init__(self, alias):
        Action.__init__(self)
        self.alias = alias


class SemCheckScope(object):
    ruleset = None
    rule = None
    term = None
    action = None

    def __init__(self):
        pass

    def EnterRuleSet(self, ruleset):
        self.ruleset = ruleset

    def ExitRuleSet(self):
        self.ruleset = None

    def EnterRule(self, rule):
        self.rule = rule

    def ExitRule(self):
        self.rule = None

    def EnterTerm(self, term):
        self.term = term

    def ExitTerm(self):
        self.term = None

    def EnterAction(self, action):
        self.action = action

    def ExitAction(self):
        self.action = None

    def GetRuleIndex(self, base=0):
        try:
            return self.ruleset.rules.index(self.rule) + base
        except:
            return None

    def GetTermIndex(self, base=0):
        try:
            return self.rule.terms.index(self.term) + base
        except:
            return None

    def GetActionIndex(self, base=0):
        try:
            return self.term.actions.index(self.action) + base
        except:
            return None


class RuleCheckException(Exception):
    ruleNo = None
    termNo = None
    actionNo = None
    message = None
    
    def __init__(self, message, scope):
        self.message = message
        self.ruleNo = scope.GetRuleIndex(1)
        self.termNo = scope.GetTermIndex(1)
        self.actionNo = scope.GetActionIndex(1)
        
    def __str__(self):
        qual = []
        if self.ruleNo is not None:
            qual.append("Rule {0}".format(self.ruleNo))
        if self.termNo is not None:
            qual.append("Term {0}".format(self.termNo))
        if self.actionNo is not None:
            qual.append("Action {0}".format(self.actionNo))
        
        if len(qual) == 0:
            qual.append("Global")
        
        return "{0}: {1}".format(", ".join(qual), self.message)
