import re

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


class StartAnchorMatch(Match):
    def __init__(self):
        Match.__init__(self)


class EndAnchorMatch(Match):
    def __init__(self):
        Match.__init__(self)


class ElementaryPatternMatch(Match):
    regex = None
    error = None

    def __init__(self):
        Match.__init__(self)

    def _setPattern(self, pattern, flags=0):
        try:
            self.regex = re.compile(pattern, flags)
        except:
            self._setError("Regex /{0}/ is not valid".format(pattern));

    def _setError(self, message):
        self.error = message
        
    def semanticCheck(self, scope):
        if not self.error is None:
            raise RuleCheckException(self.error, scope)

        Match.semanticCheck(self, scope)


class FormatMatch(ElementaryPatternMatch):
    fmt_spec_error = None
    
    def __init__(self, fmt_spec):
        ElementaryPatternMatch.__init__(self)
        
        pattern = self._makePattern(fmt_spec)

        if pattern is not None:
            self._setPattern(pattern)
        else:
            self._setError("Unrecognized format specifier '{0}'".format(fmt_spec))

    def _makePattern(self, fmt_spec):
        if fmt_spec == '%ws':
            return r'(\s*)'
        
        m = re.match(r'%([0-9]*)d', fmt_spec)
        if m is not None:
            return r'([0-9]+)' if len(m.group(1)) == 0 else r'([0-9]{{{0}}})'.format(int(m.group(1)))

        m = re.match(r'%([0-9]*)c', fmt_spec)
        if m is not None:
            return r'(.)' if len(m.group(1)) == 0 else r'(.{{{0}}})'.format(int(m.group(1)))

        m = re.match(r'%([0-9]*)s', fmt_spec)
        if m is not None:
            return r'\s*(\S)' if len(m.group(1)) == 0 else r'\s*(\S{{{0}}})'.format(int(m.group(1)))
        
        return None


class LiteralMatch(ElementaryPatternMatch):
    def __init__(self, text):
        ElementaryPatternMatch.__init__(self)
        
        self._setPattern(re.escape(text))


class RegexMatch(ElementaryPatternMatch):
    def __init__(self, patt_text):
        ElementaryPatternMatch.__init__(self)

        delim_chr = patt_text[0]
        patt_text = patt_text.replace(delim_chr*2, delim_chr)
        idx = patt_text.rfind(delim_chr)
        flags = 0

        for c in patt_text[idx+1:]:
            if c == 'i':
                flags |= re.I;
            else:
                self._setError("Invalid regex flag '{0}'".format(c))
                return

        self._setPattern(patt_text[1:idx], flags)


class InsertionMatch(Match):
    def __init__(self):
        Match.__init__(self)


class InsertAliasMatch(InsertionMatch):
    alias = None
    
    def __init__(self, alias):
        InsertionMatch.__init__(self)

        self.alias = alias


class InsertLiteralMatch(InsertionMatch):
    text = None
    
    def __init__(self, text):
        InsertionMatch.__init__(self)

        self.text = text


class Action(object):
    def __init__(self):
        pass

    def semanticCheck(self, scope):
        pass


class DeleteAction(Action):
    def __init__(self):
        Action.__init__(self)


class ReplaceByLiteralAction(Action):
    text = None
    
    def __init__(self, text):
        Action.__init__(self)

        self.text = text


def is_particle(word):
    return word in ['a','an','of','with','for','in','on']


def to_title_case(s):
    words = s.split(' ')
    first = True

    for i in xrange(len(words)):
        word = words[i]
        if word == '':
            continue

        if first or not is_particle(word.lower()):
            words[i] = word.capitalize()
        else:
            words[i] = word.lower()

        first = False
    
    return ' '.join(words)


class ApplyFunctionAction(Action):
    fn = None
    error = None
    
    def __init__(self, fn_name):
        if fn_name=="title":
            self.fn = to_title_case
        elif fn_name=="trim":
            self.fn = lambda s: s.strip()
        elif fn_name=="upper" or fn_name=="toupper":
            self.fn = lambda s: s.upper()
        elif fn_name=="lower" or fn_name=="tolower":
            self.fn = lambda s: s.lower()
        else:
            self.error = "Unsupported function '{0}'".format(fn_name)
    
    def semanticCheck(self, scope):
        if not self.error is None:
            raise RuleCheckException(self.error, scope)


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
