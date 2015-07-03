# baon/core/plan/__errors__/rename_plan_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta, abstractmethod

from baon.core.errors.BAONError import BAONError


class RenamePlanError(BAONError, metaclass=ABCMeta):
    pass


class CannotSaveRenamePlanError(RenamePlanError, metaclass=ABCMeta):
    def __init__(self, filename, **extra_parameters):
        super().__init__(filename=filename, **extra_parameters)

    def _get_format_string(self):
        return "Cannot save rename plan to '{filename}' because " + self._get_reason_format_string()

    @abstractmethod
    def _get_reason_format_string(self):
        return ''


class CannotSaveRenamePlanPermissionsError(CannotSaveRenamePlanError):
    def __init__(self, filename):
        super().__init__(filename)

    def _get_reason_format_string(self):
        return 'of a permissions issue'


class CannotSaveRenamePlanFailedWritingFileError(CannotSaveRenamePlanError):
    def __init__(self, filename):
        super().__init__(filename)

    def _get_reason_format_string(self):
        return 'the file could not be written'


class CannotSaveRenamePlanOtherError(CannotSaveRenamePlanError):
    def __init__(self, filename, error):
        super().__init__(filename, inner_error=error)

    def _get_reason_format_string(self):
        return 'of an unspecified error'


class CannotLoadRenamePlanError(RenamePlanError, metaclass=ABCMeta):
    def __init__(self, filename, **extra_parameters):
        super().__init__(filename=filename, **extra_parameters)

    def _get_format_string(self):
        return "Cannot load rename plan from '{filename}' because " + self._get_reason_format_string()

    @abstractmethod
    def _get_reason_format_string(self):
        return ''


class CannotLoadRenamePlanPermissionsError(CannotLoadRenamePlanError):
    def __init__(self, filename):
        super().__init__(filename)

    def _get_reason_format_string(self):
        return 'of a permissions issue'


class CannotLoadRenamePlanFailedReadingFileError(CannotLoadRenamePlanError):
    def __init__(self, filename):
        super().__init__(filename)

    def _get_reason_format_string(self):
        return 'the file could not be read'


class CannotLoadRenamePlanInvalidFormatError(CannotLoadRenamePlanError):
    def __init__(self, filename):
        super().__init__(filename)

    def _get_reason_format_string(self):
        return 'the file is corrupt or not a BAON rename plan'


class CannotLoadRenamePlanOtherError(CannotLoadRenamePlanError):
    def __init__(self, filename, error):
        super().__init__(filename, inner_error=error)

    def _get_reason_format_string(self):
        return 'of an unspecified error'


class RenamePlanExecuteError(RenamePlanError, metaclass=ABCMeta):
    def _get_format_string(self):
        return "Failed to execute rename plan because " + self._get_reason_format_string()

    @abstractmethod
    def _get_reason_format_string(self):
        return ''


class RenamePlanExecuteFailedBecauseActionFailedError(RenamePlanExecuteError):
    def __init__(self, action_error, rollback_ok):
        super().__init__(action_error=action_error, rollback_ok=rollback_ok)

    def _get_reason_format_string(self):
        if self.args[0]['rollback_ok']:
            rollback_text = \
                'The actions up to this point were rolled back and the directory is now in its original condition.'
        else:
            rollback_text = \
                'WARNING! The actions were not rolled back successfully. THe directory may now be in an inconsistent '\
                'state. Proceed with caution.'

        return "a step failed:\n\n{action_error}\n\n" + rollback_text


class RenamePlanExecuteFailedBecauseOtherError(RenamePlanExecuteError):
    def __init__(self, error):
        super().__init__(inner_error=error)

    def _get_reason_format_string(self):
        return 'of an unspecified error'
