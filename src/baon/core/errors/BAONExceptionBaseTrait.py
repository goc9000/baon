# baon/core/errors/BAONExceptionBaseTrait.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta, abstractmethod


class BAONExceptionBaseTrait(BaseException, metaclass=ABCMeta):

    def __str__(self):
        return self._get_format_string().format(**self.args[0])

    @abstractmethod
    def _get_format_string(self):
        return ''

    def test_repr(self):
        base_tuple = (self.__class__.__name__,)

        if len(self.args[0]) > 0:
            base_tuple += (self.args[0],)

        return base_tuple
