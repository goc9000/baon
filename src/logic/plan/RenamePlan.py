# logic/plan/RenamePlan.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from RenamePlanAction import RenamePlanAction
from BasePathAction import BasePathAction
from MkDirAction import MkDirAction
from MkDirIfNotExistsAction import MkDirIfNotExistsAction
from MoveFileAction import MoveFileAction
from RmDirAction import RmDirAction
from RmDirIfEmptyAction import RmDirIfEmptyAction

from logic.baon_utils import enum_partial_paths

import os
import re
import random
import string
import codecs


class RenamePlan(object):
    base_path = None
    steps = None
    
    def __init__(self, base_path=None, files=None):
        if base_path is None:
            self.base_path = None
            self.steps = []
            return
        
        self.base_path = base_path
        self.steps = [BasePathAction(self, base_path)]
        
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
            with codecs.open(filename, 'w', 'utf-8') as f:
                f.writelines([step.representation() + os.linesep for step in self.steps])
        except Exception as e:
            try:
                os.remove(filename)
            except OSError:
                pass
            
            raise RuntimeError("Error saving rename plan to file '{0}': {1}".format(filename, str(e)))
    
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
        try:
            plan = RenamePlan()
            
            with codecs.open(filename, 'r', 'utf-8') as f:
                line_no = 1
                for line in f:
                    try:
                        plan.steps.append(RenamePlanAction.fromRepresentation(line, plan))
                    except Exception as ex:
                        raise RuntimeError("Error in line {0}: {1}".format(line_no, str(ex)))
                    
                    line_no += 1
                
            if len(plan.steps) == 0:
                raise RuntimeError("Plan file is empty")
            if not isinstance(plan.steps[0], BasePathAction):
                raise RuntimeError("Plan must begin with BasePath action")
            
            plan.base_path = plan.steps[0].path
        except Exception as e:
            raise RuntimeError("Error reading plan from '{0}': {1}".format(filename, str(e)))
        
        return plan
    
    def execute(self, on_progress=None):
        n_steps = len(self.steps)
        
        for i in xrange(n_steps):
            try:
                if on_progress is not None:
                    on_progress(i, n_steps)
                self.steps[i].execute()
            except Exception as e:
                for j in xrange(i-1, -1, -1):
                    self.steps[j].undo()
                    if on_progress is not None:
                        on_progress(j, n_steps)
                raise e
        
    def undo(self):
        for step in reversed(self.steps):
            step.undo()
    
    def _getBufferDirName(self):
        while True:
            suffix = ''.join((random.choice(string.ascii_letters+string.digits) for _ in xrange(16)))
            name = "temp_BAON_dir_structure-{0}".format(suffix)
            if not os.path.exists(os.path.join(self.base_path, name)):
                return name
    
    def _createFinalStructureInBuffer(self, buf_dir, files):
        done = set()
        created = []
        
        self.steps.append(MkDirAction(self, buf_dir))
        done.add(buf_dir)
        created.append(buf_dir)
        
        for f in files:
            for p in enum_partial_paths(f.filename):
                path = os.path.join(buf_dir, p)
                if not path in done:
                    self.steps.append(MkDirAction(self, path))
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
            for p in enum_partial_paths(f.filename):
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
            for path in enum_partial_paths(f.old_filename):
                if not path in done:
                    done.add(path)
                    dirs.append(path)
        
        for path in reversed(dirs):
            self.steps.append(RmDirIfEmptyAction(self, path))
    
    def _tearDownBuffer(self, dirs_in_buf):
        for folder in reversed(dirs_in_buf):
            self.steps.append(RmDirAction(self, folder))
