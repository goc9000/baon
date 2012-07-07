import re, os

from FileRef import FileRef

class Renamer(object):
    NON_PRINTABLE_REGEX = re.compile(ur'[\u0000-\u001f]')
    PROBLEM_CHARS_REGEX = re.compile(r'["*:<>?\/]')
    
    ruleset = None
    use_ext = None
    use_path = None
    
    def __init__(self, ruleset, use_ext=False, use_path=False):
        self.ruleset = ruleset
        self.use_ext = use_ext
        self.use_path = use_path
        
    def rename(self, what):
        single = False
        
        if isinstance(what, FileRef):
            what = [ what ]
            single = True
        
        renamed = [self._renameFile(fref) for fref in what]
        self._performVerifications(renamed)
        
        if single:
            renamed = renamed[0]
        
        return renamed
    
    def _renameFile(self, fref):
        fname = fref.filename
        
        if not self.use_path:
            path, fname = os.path.split(fname)
        if not self.use_ext:
            fname, ext = os.path.splitext(fname)
        
        error = None
        try:
            fname = self.ruleset.applyOn(fname)
            if not self.use_ext:
                fname += ext
            if not self.use_path:
                fname = os.path.join(path, fname)
        except Exception as e:
            fname = None
            error = str(e)
        
        rfref = fref.renamed(fname)
        rfref.error = error
        
        return rfref

    def _performVerifications(self, renamed):
        coll_dict = {}
        
        for rfref in renamed:
            fname = rfref.filename
            if fname is not None:
                if fname not in coll_dict:
                    coll_dict[fname] = 1
                else:
                    coll_dict[fname] += 1
        
        for rfref in renamed:
            fname = rfref.filename
            if (fname is not None) and (coll_dict[fname] > 1):
                rfref.error = "Collides with {0} other filenames".format(coll_dict[fname]-1)
            if rfref.error is None:
                rfref.error = self._checkLocalError(rfref)
            if rfref.error is None:
                rfref.warning = self._checkLocalWarning(rfref)
    
    def _checkLocalError(self, rfref):
        path = rfref.filename
        
        m = self.NON_PRINTABLE_REGEX.search(path)
        if m is not None:
            return "Non-printable character \\u{0:04x} present in filename".format(ord(m.group(0)))
        
        base, fname = os.path.split(path)
        
        if fname == '':
            return 'Filename is empty'
        if fname == '.' or fname == '..':
            return "File may not be named '.' or '..'"
        
        if base != '':
            for comp in base.split(os.sep):
                if comp == '':
                    return 'Path has empty component'
                if comp == '.' or comp == '..':
                    return "'.' or '..' components not allowed in path"
            
        if (rfref.filename != rfref.old_filename) and os.path.exists(rfref.full_path):
            return "File already exists"
        
        return None
    
    def _checkLocalWarning(self, rfref):
        path = rfref.filename
        
        base, fname = os.path.split(path)
        fname, _ = os.path.splitext(fname)
        
        for comp in path.split(os.sep):
            m = self.PROBLEM_CHARS_REGEX.search(comp)
            if m is not None:
                return "Filename contains problematic character '{0}'".format(m.group(0))
        
        if fname.startswith(' '):
            return 'Filename starts with spaces'
        if fname.endswith(' '):
            return 'Filename has spaces before extension'
        if '  ' in fname:
            return 'Filename contains double spaces'
        
        for comp in base.split(os.sep):
            if comp.startswith(' '):
                return 'Path component starts with spaces'
            if comp.endswith(' '):
                return 'Path component ends with spaces'
            if '  ' in comp:
                return 'Path component contains double spaces'
            
        return None
    