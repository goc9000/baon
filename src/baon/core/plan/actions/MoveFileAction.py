# baon/core/plan/actions/MoveFileAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.plan.actions.RenamePlanAction import RenamePlanAction
from baon.core.plan.actions.plan_action_exceptions import CannotMoveFileDoesNotExistException,\
    CannotMoveFileDestinationExistsException, CannotMoveFileNoPermissionsException, CannotMoveFileOtherErrorException
from baon.core.utils.lang_utils import is_arrayish


class MoveFileAction(RenamePlanAction):
    from_path = None
    to_path = None

    def __init__(self, from_path, to_path):
        RenamePlanAction.__init__(self)
        self.from_path = from_path
        self.to_path = to_path

    def json_representation(self):
        return self.action_name_for_json_representation(), self.from_path, self.to_path

    def execute(self):
        try:
            if not os.path.exists(self.from_path):
                raise CannotMoveFileDoesNotExistException(self.from_path, self.to_path)
            if os.path.exists(self.to_path):
                raise CannotMoveFileDestinationExistsException(self.from_path, self.to_path)

            os.rename(self.from_path, self.to_path)
        except PermissionError:
            raise CannotMoveFileNoPermissionsException(self.from_path, self.to_path)
        except OSError as e:
            raise CannotMoveFileOtherErrorException(self.from_path, self.to_path, e)

    def undo(self):
        try:
            os.rename(self.to_path, self.from_path)
            return True
        except OSError:
            return False

    @classmethod
    def from_json_representation(cls, json_repr):
        if not is_arrayish(json_repr):
            raise RuntimeError('JSON representation of action should be a vector')
        if len(json_repr) != 3:
            raise RuntimeError('JSON representation of action has incorrect length')

        action_type, from_path, to_path = json_repr

        if action_type != cls.action_name_for_json_representation():
            raise RuntimeError("Expected JSON representation to start with '{0}' for this action".format(action_type))

        return cls(from_path, to_path)
