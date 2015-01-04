# baon/core/plan/RenamePlan.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os
import re
import random
import string
import codecs
import json

from baon.core.utils.baon_utils import enum_partial_paths
from baon.core.utils.lang_utils import is_arrayish
from baon.core.plan.actions.RenamePlanAction import RenamePlanAction
from baon.core.plan.actions.MkDirAction import MkDirAction
from baon.core.plan.actions.MkDirIfNotExistsAction import MkDirIfNotExistsAction
from baon.core.plan.actions.MoveFileAction import MoveFileAction
from baon.core.plan.actions.RmDirAction import RmDirAction
from baon.core.plan.actions.RmDirIfEmptyAction import RmDirIfEmptyAction


class RenamePlan(object):
    steps = None
    
    def __init__(self, base_path=None, files=None):
        self.steps = []

        if base_path is None:
            return

        if any(ren.error is not None for ren in files):
            raise RuntimeError("There are unresolved errors in the renamed files list")
        
        files = filter(lambda f: f.changed(), files)
        if len(files) == 0:
            raise RuntimeError("Nothing to do!")
        
        buf_dir = self._get_buffer_dir_name(base_path)
        dirs_in_buf = self._create_final_structure_in_buffer(buf_dir, files)
        self._move_files_to_buffer(base_path, buf_dir, files)
        self._merge_final_structure(base_path, files)
        self._move_files_to_destination(base_path, buf_dir, files)
        self._remove_original_dirs(base_path, files)
        self._tear_down_buffer(dirs_in_buf)

    def json_representation(self):
        return [step.json_representation() for step in self.steps]

    @staticmethod
    def from_json_representation(json_repr):
        if not is_arrayish(json_repr):
            raise RuntimeError(u"JSON representation of plan should be a vector")

        plan = RenamePlan()
        plan.steps = [RenamePlanAction.from_json_representation(action_repr) for action_repr in json_repr]

        return plan

    def save_to_file(self, filename):
        try:
            with file(filename, 'w') as f:
                json.dump(self.json_representation(), f, indent=4)
        except Exception as e:
            try:
                os.remove(filename)
            except OSError:
                pass
            
            raise RuntimeError("Error saving rename plan to file '{0}': {1}".format(filename, str(e)))

    @staticmethod
    def load_from_file(filename):
        try:
            with codecs.open(filename, 'r', 'utf-8') as f:
                representation = json.load(f)

            return RenamePlan.from_json_representation(representation)
        except Exception as e:
            raise RuntimeError("Error reading plan from '{0}': {1}".format(filename, str(e)))

    def get_backup_filename(self):
        while True:
            suffix = ''.join((random.choice(string.ascii_letters+string.digits) for _ in xrange(16)))
            name = os.path.join(os.path.expanduser('~'), "temp_BAON_rename_plan-{0}".format(suffix))
            if not os.path.exists(name):
                return name

    @staticmethod
    def find_backups():
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
    
    def _get_buffer_dir_name(self, base_path):
        while True:
            suffix = ''.join((random.choice(string.ascii_letters+string.digits) for _ in xrange(16)))
            name = "temp_BAON_dir_structure-{0}".format(suffix)

            path = os.path.join(base_path, name)
            if not os.path.exists(path):
                return path
    
    def _create_final_structure_in_buffer(self, buf_dir, files):
        done = set()
        created = []
        
        self.steps.append(MkDirAction(buf_dir))
        done.add(buf_dir)
        created.append(buf_dir)
        
        for f in files:
            for p in enum_partial_paths(f.filename):
                path = os.path.join(buf_dir, p)
                if not path in done:
                    self.steps.append(MkDirAction(path))
                    done.add(path)
                    created.append(path)
        
        return created
    
    def _move_files_to_buffer(self, base_path, buf_dir, files):
        for f in files:
            self.steps.append(MoveFileAction(os.path.join(base_path, f.old_filename),
                                             os.path.join(buf_dir, f.filename)))
    
    def _merge_final_structure(self, base_path, files):
        done = set()
        
        for f in files:
            for p in enum_partial_paths(f.filename):
                if not p in done:
                    path = os.path.join(base_path, p)
                    if not os.path.isdir(path):
                        self.steps.append(MkDirIfNotExistsAction(path))
                    done.add(p)
    
    def _move_files_to_destination(self, base_path, buf_dir, files):
        for f in files:
            self.steps.append(MoveFileAction(os.path.join(buf_dir, f.filename),
                                             os.path.join(base_path, f.filename)))
    
    def _remove_original_dirs(self, base_path, files):
        done = set()
        dirs = []
        
        for f in files:
            for path in enum_partial_paths(f.old_filename):
                if not path in done:
                    done.add(path)
                    dirs.append(path)
        
        for path in reversed(dirs):
            self.steps.append(RmDirIfEmptyAction(os.path.join(base_path, path)))
    
    def _tear_down_buffer(self, dirs_in_buf):
        for folder in reversed(dirs_in_buf):
            self.steps.append(RmDirAction(folder))
