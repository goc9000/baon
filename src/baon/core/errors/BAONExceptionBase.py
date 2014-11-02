# baon/core/errors/BAONExceptionBase.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


class BAONExceptionBase(Exception):
    format_string = None
    error_parameters = None
    
    def __init__(self, format_string, error_parameters=None):
        self.format_string = format_string
        self.error_parameters = error_parameters if error_parameters is not None else dict()
        Exception.__init__(self, format_string.format(**error_parameters))

    def __str__(self):
        return self.format_string.format(**self.error_parameters)

    def test_repr(self):
        base_tuple = (self.__class__.__name__,)

        if len(self.error_parameters) > 0:
            base_tuple += (self.error_parameters,)

        return base_tuple
