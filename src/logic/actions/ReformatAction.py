from Action import Action
from logic.errors.RuleCheckException import RuleCheckException
from logic.errors.RuleApplicationException import RuleApplicationException
import re

def strip_zeroes(s):
    m = re.match(r'(\s*)([0-9]+)(\s*)', s)
    
    if m is None:
        raise RuleApplicationException("%d applied to non-number")
    
    mid = m.group(2).lstrip('0')
    if mid == '':
        mid = '0'
    
    return m.group(1)+mid+m.group(3)

def pad_with_zeroes(s, digits):
    m = re.match(r'(\s*)([0-9]+)(\s*)', s)
    
    if m is None:
        raise RuleApplicationException("%Nd applied to non-number")
    
    mid = m.group(2).lstrip('0')
    if mid == '':
        mid = '0'

    mid = mid.zfill(digits)

    return m.group(1)+mid+m.group(3)

class ReformatAction(Action):
    error = None
    fn = None
    
    def __init__(self, fmt_spec):
        Action.__init__(self)
        
        self.fn = self._selectFunction(fmt_spec)
        if self.fn is None:
            self.error="Unrecognized format specifier '{0}'".format(fmt_spec)
 
    def _selectFunction(self, fmt_spec):
        if fmt_spec == '%d':
            return lambda s, c: strip_zeroes(s)
        
        m = re.match(r'%([0-9]*)d', fmt_spec)
        if m is not None:
            digits = int(m.group(1))
            return lambda s, c: pad_with_zeroes(s, digits)
        
        return None
        
    def semanticCheck(self, scope):
        Action.semanticCheck(self, scope)
        
        if not self.error is None:
            raise RuleCheckException(self.error, scope)

    def execute(self, text, context):
        return self.fn(text, context)
    