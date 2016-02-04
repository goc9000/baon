# baon/core/plan/DeleteEmptyDirectoryAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.plan.actions.RenamePlanAction import RenamePlanAction
from baon.core.plan.actions.__errors__.plan_action_errors import CannotDeleteDirDoesNotExistError,\
    CannotDeleteDirIsAFileError, CannotDeleteDirNoPermissionsError, CannotDeleteDirOtherError, \
    CannotDeleteDirNotEmptyError
from baon.core.utils.lang_utils import is_arrayish


class DeleteEmptyDirectoryAction(RenamePlanAction):
    path = None

    def __init__(self, path):
        RenamePlanAction.__init__(self)
        self.path = path

    def execute(self):
        try:
            if len(os.listdir(self.path)) > 0:
                raise CannotDeleteDirNotEmptyError(self.path)

            os.rmdir(self.path)
        except NotADirectoryError:
            raise CannotDeleteDirIsAFileError(self.path) from None
        except FileNotFoundError:
            raise CannotDeleteDirDoesNotExistError(self.path) from None
        except PermissionError:
            raise CannotDeleteDirNoPermissionsError(self.path) from None
        except OSError as e:
            raise CannotDeleteDirOtherError(self.path, e) from None

    def undo(self):
        try:
            os.mkdir(self.path)
            return True
        except OSError:
            return False

    def json_representation(self):
        return self.action_name_for_json_representation(), self.path

    @classmethod
    def from_json_representation(cls, json_repr):
        if not is_arrayish(json_repr):
            raise ValueError('JSON representation of action should be a vector')
        if len(json_repr) != 2:
            raise ValueError('JSON representation of action has incorrect length')

        action_type, path = json_repr

        if action_type != cls.action_name_for_json_representation():
            raise ValueError("Expected JSON representation to start with '{0}' for this action".format(action_type))

        return cls(path)
