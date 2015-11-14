# baon/core/plan/DeleteDirectoryIfEmptyAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.plan.actions.RenamePlanAction import RenamePlanAction
from baon.core.plan.actions.__errors__.plan_action_errors import CannotDeleteDirDoesNotExistError,\
    CannotDeleteDirIsAFileError, CannotDeleteDirNoPermissionsError, CannotDeleteDirOtherError
from baon.core.utils.lang_utils import is_arrayish


class DeleteDirectoryIfEmptyAction(RenamePlanAction):
    path = None
    
    def __init__(self, path):
        RenamePlanAction.__init__(self)
        self.path = path

    def execute(self):
        try:
            if os.path.isfile(self.path):
                raise CannotDeleteDirIsAFileError(self.path)
            if not os.path.exists(self.path):
                raise CannotDeleteDirDoesNotExistError(self.path)

            is_empty = (len(os.listdir(self.path)) == 0)
            if not is_empty:
                return

            os.rmdir(self.path)
        except PermissionError:
            raise CannotDeleteDirNoPermissionsError(self.path) from None
        except OSError as e:
            raise CannotDeleteDirOtherError(self.path, e) from None

    def undo(self):
        try:
            if os.path.isdir(self.path) and len(os.listdir(self.path)) > 0:
                return None

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
