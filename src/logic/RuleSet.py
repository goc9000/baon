class RuleSet(object):
    rules = None
    
    def __init__(self):
        self.rules = []

    def isEmpty(self):
        return len(self.rules) == 0
    
    def semanticCheck(self, scope=None):
        if scope is None:
            scope = SemanticCheckScope
        
        for rule in self.rules:
            rule.semanticCheck(scope)


class Rule(object):
    alternatives = None
    
    def __init__(self):
        self.alternatives = []

    def semanticCheck(self, scope):
        for alt in self.alternatives:
            alt.semanticCheck(scope)


class MatchSequence(object):
    terms = None

    def __init__(self):
        self.terms = []

    def semanticCheck(self, scope):
        #todo: check for consecutive '..' s etc.
        
        for term in self.terms:
            term.semanticCheck(scope)


class Match(object):
    actions = None

    def __init__(self):
        self.actions = []

    def semanticCheck(self, scope):
        # This just checks the actions
        for action in self.actions:
            action.semanticCheck(scope)


class FormatMatch(Match):
    fmt_spec_error = None
    
    def __init__(self, fmt_spec):
        Match.__init__(self)

        # If format specifier is invalid, fail silently; error will be reported upon a semantic check
        self.fmt_spec_error = "Unrecognized format specifier '{0}'".format(fmt_spec)

    def semanticCheck(self, scope):
        Match.semanticCheck(self, scope)

        if not self.fmt_spec_error is None:
            raise RuleCheckException(self.fmt_spec_error, scope)


class SemanticCheckScope(object):
    def __init__(self):
        pass


class RuleCheckException(Exception):
    message = None
    scope = None
    
    def __init__(self, message, scope):
        self.message = message
        self.scope = scope
    
    def __str__(self):
        return self.message
