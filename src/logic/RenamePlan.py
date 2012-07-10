import os, re, random, string

PAT_WS = re.compile(r'\s*')
PAT_FIRST_KW = re.compile(r'([\w]+)\s*')
PAT_QUOTED = re.compile(r'\s*"((\\"|[^"])*)"\s*')

def parse_plan_file_line(line):
    m = PAT_FIRST_KW.match(line)
    if m is None:
        raise RuntimeError("No starting keyword")
    kw = m.group(1)
    
    params = []
    pos = len(m.group(0))
    while True:
        pos += len(PAT_WS.match(line, pos).group(0))
        if pos == len(line):
            break
        
        m = PAT_QUOTED.match(line, pos)
        if m is None:
            raise RuntimeError("Error in format")
        
        params.append(unescape_str(m.group(1)))
        
        pos += len(m.group(0))
        
    return (kw, params)

def escape_str(text):
    return text.replace("\\", "\\\\").replace('"', '\\"')

def unescape_str(text):
    return text.replace('\\"', '"').replace("\\\\","\\")

class RenamePlan(object):
    base_path = None
    steps = None
    
    def __init__(self, base_path, files=None):
        self.base_path = base_path
        self.steps = []

        if files is None:
            return
        
        if any(ren.error is not None for ren in files):
            raise RuntimeError("There are unresolved errors in the renamed files list")
        
        files = filter(lambda f: f.changed(), files)
        if len(files) == 0:
            raise RuntimeError("Nothing to do!")
        
        buf_dir = self._getBufferDirName()
        dirs_in_buf = self._createFinalStructureInBuffer(buf_dir, files)
        self._moveFilesToBuffer(buf_dir, files)
        self._mergeFinalStructure(buf_dir, files)
        self._moveFilesToDestination(buf_dir, files)
        self._removeOriginalDirs(files)
        self._tearDownBuffer(dirs_in_buf)
    
    def saveToFile(self, filename):
        try:
            with file(filename, "w+") as f:
                f.writelines(self._genFileLines())
        except Exception:
            try:
                os.remove(filename)
            except:
                pass
            
            raise RuntimeError("Error saving rename plan to file '{0}'", filename)
    
    def _genFileLines(self):
        yield 'BasePath "{0}"'.format(escape_str(self.base_path)) + os.linesep
        
        for step in self.steps:
            yield repr(step) + os.linesep
    
    def getBackupFileName(self):
        while True:
            suffix = ''.join((random.choice(string.ascii_letters+string.digits) for _ in xrange(16)))
            name = os.path.join(os.path.expanduser('~'), "temp_BAON_rename_plan-{0}".format(suffix))
            if not os.path.exists(name):
                return name
    
    @staticmethod
    def findBackups():
        try:
            home_dir = os.path.expanduser('~')
            files = os.listdir(home_dir)
            
            for filename in files:
                path = os.path.join(home_dir, filename)
                if re.match(r"temp_BAON_rename_plan-", filename) and os.path.isfile(path):
                    return path
        except Exception:
            raise RuntimeError("Could not look for backups in home directory!")
    
        return None
    
    @staticmethod
    def loadFromFile(filename):
        param_counts = { \
            'BasePath': 1,
            'MkDirIfNotExists': 1,
            'MoveFile': 2,
            'RmDirIfEmpty': 1,
            'RmDir' : 1
        }
        
        try:
            with file(filename, "r") as f:
                line_no = 1
                for line in f:
                    try:
                        kw, params = parse_plan_file_line(line)
                        
                        if kw not in param_counts:
                            raise RuntimeError("Unknown keyword '{0}'".format(kw))
                        if len(params) != param_counts[kw]:
                            raise RuntimeError("Expected {0} parameters for '{1}', got {2}".format(param_counts[kw], kw, len(params)))
                        
                        if line_no == 1:
                            if kw != 'BasePath':
                                raise RuntimeError("Expected keyword 'BasePath'")
                            plan = RenamePlan(params[0])
                        else:
                            if kw == 'MkDirIfNotExists':
                                plan.steps.append(MkDirIfNotExistsAction(plan, params[0]))
                            if kw == 'MoveFile':
                                plan.steps.append(MoveFileAction(plan, params[0], params[1]))
                            if kw == 'RmDirIfEmpty':
                                plan.steps.append(RmDirIfEmptyAction(plan, params[0]))
                            if kw == 'RmDir':
                                plan.steps.append(RmDirAction(plan, params[0]))
                    except Exception as ex:
                        raise RuntimeError("Error in line {0}: {1}".format(line_no, str(ex)))
                    
                    line_no += 1
                
                if line_no == 1:
                    raise RuntimeError("File is empty!")
        except Exception as e:
            raise RuntimeError("Error reading plan from '{0}': {1}".format(filename, str(e)))
        
        return plan
    
    def execute(self):
        raise RuntimeError("RenamePlan.execute NIY")
        
    def undo(self):
        raise RuntimeError("RenamePlan.undo NIY")
    
    def _getBufferDirName(self):
        while True:
            suffix = ''.join((random.choice(string.ascii_letters+string.digits) for _ in xrange(16)))
            name = "temp_BAON_dir_structure-{0}".format(suffix)
            if not os.path.exists(os.path.join(self.base_path, name)):
                return name
    
    def _createFinalStructureInBuffer(self, buf_dir, files):
        done = set()
        created = []
        
        self.steps.append(MkDirIfNotExistsAction(self, buf_dir))
        done.add(buf_dir)
        created.append(buf_dir)
        
        for f in files:
            for p in self._allParents(f.filename):
                path = os.path.join(buf_dir, p)
                if not path in done:
                    self.steps.append(MkDirIfNotExistsAction(self, path))
                    done.add(path)
                    created.append(path)
        
        return created
    
    def _moveFilesToBuffer(self, buf_dir, files):
        for f in files:
            self.steps.append(MoveFileAction(self, f.old_filename,
                                             os.path.join(buf_dir, f.filename)))
    
    def _mergeFinalStructure(self, buf_dir, files):
        done = set()
        
        for f in files:
            for p in self._allParents(f.filename):
                if not p in done:
                    if not os.path.isdir(os.path.join(self.base_path, p)):
                        self.steps.append(MkDirIfNotExistsAction(self, p))
                    done.add(p)
    
    def _moveFilesToDestination(self, buf_dir, files):
        for f in files:
            self.steps.append(MoveFileAction(self, os.path.join(buf_dir, f.filename),
                                             f.filename))
    
    def _removeOriginalDirs(self, files):
        done = set()
        dirs = []
        
        for f in files:
            for path in self._allParents(f.old_filename):
                if not path in done:
                    done.add(path)
                    dirs.append(path)
        
        for path in reversed(dirs):
            self.steps.append(RmDirIfEmptyAction(self, path))
    
    def _tearDownBuffer(self, dirs_in_buf):
        for folder in reversed(dirs_in_buf):
            self.steps.append(RmDirAction(self, folder))
    
    def _allParents(self, filename):
        base = ''
        
        path, _ = os.path.split(filename)
        
        if path != '':
            for comp in path.split(os.sep):
                base = os.path.join(base, comp)
                yield base
    
    def __str__(self):
        return '\n'.join([str(step) for step in self.steps])

class MkDirIfNotExistsAction(object):
    plan = None
    directory = None
    
    def __init__(self, plan, directory):
        self.plan = plan
        self.directory = directory
    
    def __repr__(self):
        return 'MkDirIfNotExists "{0}"'.format(escape_str(self.directory))

class MoveFileAction(object):
    plan = None
    from_path = None
    to_path = None
    
    def __init__(self, plan, from_path, to_path):
        self.plan = plan
        self.from_path = from_path
        self.to_path = to_path
    
    def __repr__(self):
        return 'MoveFile "{0}" "{1}"'.format(escape_str(self.from_path), escape_str(self.to_path))

class RmDirAction(object):
    plan = None
    directory = None
    
    def __init__(self, plan, directory):
        self.plan = plan
        self.directory = directory
    
    def __repr__(self):
        return 'RmDir "{0}"'.format(escape_str(self.directory))

class RmDirIfEmptyAction(object):
    plan = None
    directory = None
    
    def __init__(self, plan, directory):
        self.plan = plan
        self.directory = directory
    
    def __repr__(self):
        return 'RmDirIfEmpty "{0}"'.format(escape_str(self.directory))
