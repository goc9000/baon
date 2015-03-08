# baon/core/plan/actions/RenamePlanAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import re

from abc import ABCMeta, abstractmethod

from baon.core.utils.lang_utils import is_arrayish, iter_non_abstract_descendants


class RenamePlanAction(object, metaclass=ABCMeta):
    def __init__(self):
        pass

    def __eq__(self, other):
        return self.json_representation() == other.json_representation()

    def test_repr(self):
        return self.json_representation()

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        """
        Undoes the action.

        Returns True if the action had been executed and has been successfully undone; False if the action had not
        been executed and/or there was a problem undoing it; or None if the action, as well as undoing it, would be
        a no-op.
        """
        return None

    @abstractmethod
    def json_representation(self):
        return ()

    @classmethod
    def action_name_for_json_representation(cls):
        match = re.match('^(.*)Action$', cls.__name__)
        assert match is not None

        return match.group(1)

    @classmethod
    def from_json_representation(cls, json_repr):
        if not is_arrayish(json_repr):
            raise ValueError('JSON representation of action should be a vector')
        if len(json_repr) == 0:
            raise ValueError('JSON representation of action should start with the action type')

        action_type = json_repr[0]
        action_class = get_action_class(action_type)

        return action_class.from_json_representation(json_repr)


action_class_lookup = None


def get_action_class(action_type):
    global action_class_lookup

    if action_class_lookup is None:
        action_class_lookup = {
            cls.action_name_for_json_representation(): cls for cls in iter_non_abstract_descendants(RenamePlanAction)
        }

    cls = action_class_lookup.get(action_type)
    if cls is None:
        raise ValueError("Unrecognized action: '{0}'".format(action_type))

    return cls
