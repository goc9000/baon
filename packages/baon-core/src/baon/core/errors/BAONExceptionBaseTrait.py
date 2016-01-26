# baon/core/errors/BAONExceptionBaseTrait.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta, abstractmethod

from baon.core.utils.lang_utils import is_arrayish


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

    @staticmethod
    def from_test_repr(error_repr):
        assert is_arrayish(error_repr)
        assert len(error_repr) > 0

        error_class = error_repr[0]

        assert error_class in ['SyntheticFileError', 'SyntheticFileWarning'],\
            'Only SyntheticFileError and SyntheticFileWarning are supported'

        if error_class == 'SyntheticFileError':
            from baon.core.files.__errors__.file_reference_errors import SyntheticFileError
            return SyntheticFileError()
        elif error_class == 'SyntheticFileWarning':
            from baon.core.files.__errors__.file_reference_errors import SyntheticFileWarning
            return SyntheticFileWarning()
