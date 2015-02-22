# baon/core/plan/RenamePlan.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os
import json

from baon.core.plan.__errors__.rename_plan_errors import CannotSaveRenamePlanFailedWritingFileError,\
    CannotSaveRenamePlanPermissionsError, CannotSaveRenamePlanOtherError, CannotLoadRenamePlanFailedReadingFileError,\
    CannotLoadRenamePlanInvalidFormatError, CannotLoadRenamePlanPermissionsError, CannotLoadRenamePlanOtherError, \
    RenamePlanExecuteFailedBecauseActionFailedError, RenamePlanExecuteFailedBecauseOtherError

from baon.core.plan.actions.__errors__.plan_action_errors import RenamePlanActionError

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
        last_successful_step = None

        try:
            for i in range(n_steps):
                if on_progress is not None:
                    on_progress(i, n_steps)

                self.steps[i].execute()

                last_successful_step = i
        except Exception as e:
            rollback_ok = self._undo(from_step=last_successful_step) if last_successful_step is not None else True

            try:
                raise e
            except RenamePlanActionError as action_error:
                raise RenamePlanExecuteFailedBecauseActionFailedError(action_error, rollback_ok) from None
            except Exception as e:
                raise RenamePlanExecuteFailedBecauseOtherError(e) from None

    def undo(self):
        return self._undo()

    def undo_partial_execution(self):
        return self._undo(initial_failures_ok=True)

    def _undo(self, from_step=None, initial_failures_ok=False):
        steps_to_undo = self.steps if from_step is None else self.steps[:from_step + 1]
        allow_errors = initial_failures_ok
        general_success = True

        for step in reversed(steps_to_undo):
            if not step.undo():
                if not allow_errors:
                    general_success = False
            else:
                allow_errors = False

            # Note: we intentionally plow through even if some undo actions failed

        return general_success

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
