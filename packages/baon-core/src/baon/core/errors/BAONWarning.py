# baon/core/errors/BAONWarning.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta

from baon.core.errors.BAONExceptionBaseTrait import BAONExceptionBaseTrait


class BAONWarning(BAONExceptionBaseTrait, Warning, metaclass=ABCMeta):

    def __init__(self, **error_parameters):
        BAONExceptionBaseTrait.__init__(self)
        Warning.__init__(self, error_parameters)
