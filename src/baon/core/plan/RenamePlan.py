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
import json

from baon.core.plan.__errors__.rename_plan_errors import CannotSaveRenamePlanFailedWritingFileError,\
    CannotSaveRenamePlanPermissionsError, CannotSaveRenamePlanOtherError, CannotLoadRenamePlanFailedReadingFileError,\
    CannotLoadRenamePlanInvalidFormatError, CannotLoadRenamePlanPermissionsError, CannotLoadRenamePlanOtherError

from baon.core.utils.lang_utils import is_arrayish, is_dictish, is_string, swallow_os_errors
from baon.core.plan.actions.RenamePlanAction import RenamePlanAction


class RenamePlan(object):
    steps = None
    comment = None
    
    def __init__(self, steps, comment=None):
        self.steps = steps
        self.comment = comment

    def __eq__(self, other):
        return \
            (len(self.steps) == len(other.steps)) and \
            all(step == other_step for step, other_step in zip(self.steps, other.steps))

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
        return tuple(step.json_representation() for step in self.steps)

    def json_representation(self):
        representation = {
            'steps': [step.json_representation() for step in self.steps],
        }

        if self.comment is not None:
            representation['comment'] = self.comment

        return representation

    @staticmethod
    def from_json_representation(json_repr):
        if not is_dictish(json_repr):
            raise ValueError("JSON representation of plan should be a dictionary")

        if 'steps' not in json_repr:
            raise ValueError("Missing top-level field 'steps'")
        steps_repr = json_repr['steps']
        if not is_arrayish(steps_repr):
            raise ValueError("Expected vector for 'steps' field")
        steps = [RenamePlanAction.from_json_representation(action_repr) for action_repr in steps_repr]

        comment = None
        if 'comment' in json_repr:
            if not is_string(json_repr['comment']):
                raise ValueError("Expected stirng for 'comment' field")
            comment = json_repr['comment']

        return RenamePlan(steps, comment)

    def save_to_file(self, filename, comment=None):
        success = False

        try:
            json_repr = self.json_representation()

            # Override saved comment without changing .comment field in plan
            if comment is not None:
                json_repr['comment'] = comment

            with open(filename, 'wt') as f:
                json.dump(self.json_representation(), f, indent=4)

            success = True
        except PermissionError:
            raise CannotSaveRenamePlanPermissionsError(filename) from None
        except OSError:
            raise CannotSaveRenamePlanFailedWritingFileError(filename) from None
        except Exception as e:
            raise CannotSaveRenamePlanOtherError(filename, e) from None
        finally:
            if not success:
                with swallow_os_errors():
                    os.remove(filename)

    @staticmethod
    def load_from_file(filename):
        try:
            with open(filename, 'rt') as f:
                representation = json.load(f)

                return RenamePlan.from_json_representation(representation)
        except PermissionError:
            raise CannotLoadRenamePlanPermissionsError(filename) from None
        except OSError:
            raise CannotLoadRenamePlanFailedReadingFileError(filename) from None
        except ValueError as e:
            raise CannotLoadRenamePlanInvalidFormatError(filename) from None
        except Exception as e:
            raise CannotLoadRenamePlanOtherError(filename, e) from None

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
