# baon/core/plan/actions/CreateDirectoryAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.plan.actions.RenamePlanAction import RenamePlanAction
from baon.core.plan.actions.plan_action_exceptions import CannotCreateDirAlreadyExistsException,\
    CannotCreateDirFileInWayException, CannotCreateDirParentDoesNotExistException,\
    CannotCreateDirParentNotADirectoryException, CannotCreateDirNoPermissionsException,\
    CannotCreateDirOtherErrorException
from baon.core.utils.lang_utils import is_arrayish


class CreateDirectoryAction(RenamePlanAction):
    path = None
    
    def __init__(self, path):
        RenamePlanAction.__init__(self)
        self.path = path
    
    def json_representation(self):
        return self.action_name_for_json_representation(), self.path

    def execute(self):
        try:
            if os.path.isfile(self.path):
                raise CannotCreateDirFileInWayException(self.path)
            if os.path.exists(self.path):
                raise CannotCreateDirAlreadyExistsException(self.path)

            parent_path, _ = os.path.split(self.path)

            if not os.path.exists(parent_path):
                raise CannotCreateDirParentDoesNotExistException(self.path)
            if os.path.isfile(parent_path):
                raise CannotCreateDirParentNotADirectoryException(self.path)

            os.mkdir(self.path)
        except PermissionError:
            raise CannotCreateDirNoPermissionsException(self.path) from None
        except OSError as e:
            raise CannotCreateDirOtherErrorException(self.path, e) from None

    def undo(self):
        try:
            os.rmdir(self.path)
            return True
        except OSError:
            return False

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
