# baon/core/plan/actions/MoveFileAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.plan.actions.RenamePlanAction import RenamePlanAction
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
                raise RuntimeError("source does not exist")
            if os.path.exists(self.to_path):
                raise RuntimeError("destination already exists")
            
            os.rename(self.from_path, self.to_path)
        except Exception as e:
            raise RuntimeError("Cannot move '{0}' to '{1}': {2}".format(self.from_path, self.to_path, str(e)))
    
    def undo(self):
        try:
            if os.path.exists(self.to_path) and not os.path.exists(self.from_path):
                os.rename(self.to_path, self.from_path)
        except OSError:
            pass

    @classmethod
    def from_json_representation(cls, json_repr):
        if not is_arrayish(json_repr):
            raise RuntimeError(u'JSON representation of action should be a vector')
        if len(json_repr) != 3:
            raise RuntimeError(u'JSON representation of action has incorrect length')

        action_type, from_path, to_path = json_repr

        if action_type != cls.action_name_for_json_representation():
            raise RuntimeError(u"Expected JSON representation to start with '{0}' for this action".format(action_type))

        return cls(from_path, to_path)
