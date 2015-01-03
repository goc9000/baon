# baon/core/errors/BAONWarningBase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONExceptionBaseTrait import BAONExceptionBaseTrait


class BAONWarningBase(Warning, BAONExceptionBaseTrait):

    def __init__(self, format_string, error_parameters=None):
        BAONExceptionBaseTrait.__init__(self, format_string, error_parameters)
        Warning.__init__(self, format_string.format(**self.error_parameters))