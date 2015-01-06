# baon/core/plan/actions/RenamePlanAction.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import re

from abc import ABCMeta, abstractmethod
from collections import deque
from inspect import isabstract

from baon.core.utils.lang_utils import is_arrayish


class RenamePlanAction(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def test_repr(self):
        return self.json_representation()

    @abstractmethod
    def json_representation(self):
        return ()

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

    @classmethod
    def action_name_for_json_representation(cls):
        match = re.match(u'^(.*)Action$', cls.__name__)
        assert match is not None

        return match.group(1)

    @classmethod
    def from_json_representation(cls, json_repr):
        if not is_arrayish(json_repr):
            raise RuntimeError(u'JSON representation of action should be a vector')
        if len(json_repr) == 0:
            raise RuntimeError(u'JSON representation of action should start with the action type')

        action_type = json_repr[0]
        action_class = get_action_class(action_type)

        return action_class.from_json_representation(json_repr)


action_class_lookup = None


def get_action_class(action_type):
    global action_class_lookup

    if action_class_lookup is None:
        action_class_lookup = {}

        q = deque()
        q.append(RenamePlanAction)

        while len(q) > 0:
            cls = q.popleft()
            q.extend(cls.__subclasses__())

            if not isabstract(cls):
                action_class_lookup[cls.action_name_for_json_representation()] = cls

    cls = action_class_lookup.get(action_type)
    if cls is None:
        raise RuntimeError(u"Unrecognized action: '{0}'".format(action_type))

    return cls
