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

from baon.core.utils.lang_utils import is_arrayish, swallow_os_errors
from baon.core.plan.actions.RenamePlanAction import RenamePlanAction


class RenamePlan(object):
    steps = None
    
    def __init__(self, steps):
        self.steps = steps

    def execute(self, on_progress=None):
        n_steps = len(self.steps)

        for i in range(n_steps):
            try:
                if on_progress is not None:
                    on_progress(i, n_steps)
                self.steps[i].execute()
            except Exception as e:
                for j in range(i-1, -1, -1):
                    self.steps[j].undo()
                    if on_progress is not None:
                        on_progress(j, n_steps)
                raise e

    def undo(self):
        for step in reversed(self.steps):
            step.undo()

    def test_repr(self):
        return tuple(self.json_representation())

    def json_representation(self):
        return [step.json_representation() for step in self.steps]

    @staticmethod
    def from_json_representation(json_repr):
        if not is_arrayish(json_repr):
            raise ValueError("JSON representation of plan should be a vector")

        return RenamePlan([RenamePlanAction.from_json_representation(action_repr) for action_repr in json_repr])

    def save_to_file(self, filename):
        try:
            with open(filename, 'w') as f:
                json.dump(self.json_representation(), f, indent=4)
        except Exception as e:
            with swallow_os_errors():
                os.remove(filename)
            
            raise e

    @staticmethod
    def load_from_file(filename):
        with codecs.open(filename, 'r', 'utf-8') as f:
            representation = json.load(f)

        return RenamePlan.from_json_representation(representation)

    def get_backup_filename(self):
        while True:
            suffix = ''.join((random.choice(string.ascii_letters+string.digits) for _ in range(16)))
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
            raise RuntimeError("Could not look for backups in home directory!") from None

        return None
