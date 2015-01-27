# baon/core/plan/actions/CreateDirectoryAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.plan.actions.RenamePlanAction import RenamePlanAction
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
                raise RuntimeError("a file by that name already exists")
            if os.path.exists(self.path):
                raise RuntimeError("directory already exists")
            
            os.mkdir(self.path)
        except Exception as e:
            raise RuntimeError("Cannot create '{0}': {1}".format(self.path, str(e)))
    
    def undo(self):
        try:
            os.rmdir(self.path)
        except OSError:
            pass

    @classmethod
    def from_json_representation(cls, json_repr):
        if not is_arrayish(json_repr):
            raise RuntimeError('JSON representation of action should be a vector')
        if len(json_repr) != 2:
            raise RuntimeError('JSON representation of action has incorrect length')

        action_type, path = json_repr

        if action_type != cls.action_name_for_json_representation():
            raise RuntimeError("Expected JSON representation to start with '{0}' for this action".format(action_type))

        return cls(path)
