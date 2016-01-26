# baon/core/errors/BAONError.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta

from baon.core.errors.BAONExceptionBaseTrait import BAONExceptionBaseTrait


class BAONError(BAONExceptionBaseTrait, Exception, metaclass=ABCMeta):

    def __init__(self, **error_parameters):
        BAONExceptionBaseTrait.__init__(self)
        Exception.__init__(self, error_parameters)
