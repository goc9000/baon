import os

from FileRef import FileRef

class Renamer(object):
    ruleset = None
    
    def __init__(self, ruleset):
        self.ruleset = ruleset
        
    def rename(self, what):
        if isinstance(what, FileRef):
            return self._renameFile(what)
        
        return [self._renameFile(fref) for fref in what]
    
    def _renameFile(self, fref):
        try:
            text = fref.filename
            
            for rule in self.ruleset.rules:
                text, final = self._applyRule(text, rule)
                if final == True:
                    break
            
            return fref.renamed(text)
        except Exception as e:
            return e
    
    def _applyRule(self, text, rule):
        text, ext = os.path.splitext(text)

        #todo
        
        text = text + ext
        
        return (text, True)
