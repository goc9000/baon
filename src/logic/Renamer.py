import re, os

from utils import enum_partial_paths
from RenamedFileRef import RenamedFileRef

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
        
    def rename(self, files):
        renamed = [self._renameFile(fref) for fref in files]
        self._performVerifications(renamed)
        
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
        
        rfref = RenamedFileRef(fref, fname)
        rfref.error = error
        
        return rfref

    def _performVerifications(self, renamed):
        """
        Performs verifications.
        
        Note: by design, the renamer will only perform verifications that do
        not require further accesses to the filesystem. Errors that can only be
        detected by using such information will be caught in the planning phase.
        """
         
        if self._checkForIntrinsicErrors(renamed):
            return
        if self._checkForCollisions(renamed):
            return
        
    def _checkForIntrinsicErrors(self, renamed):
        errors_found = False
        
        for rfref in renamed:
            rfref.error = self._checkForIntrinsicError(rfref)
            if rfref.error is not None:
                errors_found = True
            else:
                rfref.warning = self._checkForIntrinsicWarning(rfref)

        return errors_found
    
    def _checkForIntrinsicError(self, rfref):
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
        
        return None
    
    def _checkForIntrinsicWarning(self, rfref):
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
    
    def _checkForCollisions(self, renamed):
        errors_found = False
        
        dest_use_counts = dict()
        partial_paths = set()
        
        for rfref in renamed:
            if rfref.filename not in dest_use_counts:
                dest_use_counts[rfref.filename] = list([0, 0])
            
            dest_use_counts[rfref.filename][1 if rfref.is_dir else 0] += 1
            
            for path in enum_partial_paths(rfref.filename):
                partial_paths.add(path)
        
        for rfref in renamed:
            uses = dest_use_counts[rfref.filename]
            if rfref.is_dir:
                if uses[0] > 0:
                    rfref.error = "Collides with file"
                elif uses[1] > 1:
                    rfref.error = "Would merge implicitly with other folders"
            else:
                if uses[0] > 1:
                    rfref.error = "Collides with other files"
                elif uses[1] > 0:
                    rfref.error = "Collides with directory"
            
            if rfref.filename in partial_paths:
                if rfref.is_dir:
                    rfref.error = "Would merge implicitly with other folders"
                else:
                    rfref.error = "Collides with directory in final structure"
            
            if rfref.error is not None:
                errors_found = True
        
        return errors_found
