# baon/core/plan/__errors__/rename_plan_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONError import BAONError


class RenamePlanError(BAONError):
    def __init__(self, format_string, error_parameters=None):
        BAONError.__init__(self, format_string, error_parameters)


class CannotSaveRenamePlanError(RenamePlanError):
    def __init__(self, filename, reason_format_string, reason_parameters=None):
        reason_parameters = dict(reason_parameters or dict())
        reason_parameters['filename'] = filename

        RenamePlanError.__init__(
            self,
            "Cannot save rename plan to '{filename}' because " + reason_format_string,
            reason_parameters)


class CannotSaveRenamePlanPermissionsError(CannotSaveRenamePlanError):
    def __init__(self, filename):
        CannotSaveRenamePlanError.__init__(
            self,
            filename,
            'of a permissions issue')


class CannotSaveRenamePlanFailedWritingFileError(CannotSaveRenamePlanError):
    def __init__(self, filename):
        CannotSaveRenamePlanError.__init__(
            self,
            filename,
            "the file could not be written")


class CannotSaveRenamePlanOtherError(CannotSaveRenamePlanError):
    def __init__(self, filename, error):
        CannotSaveRenamePlanError.__init__(
            self,
            filename,
            'of an unspecified error',
            {'inner_error': error})


class CannotLoadRenamePlanError(RenamePlanError):
    def __init__(self, filename, reason_format_string, reason_parameters=None):
        reason_parameters = dict(reason_parameters or dict())
        reason_parameters['filename'] = filename

        RenamePlanError.__init__(
            self,
            "Cannot load rename plan from '{filename}' because " + reason_format_string,
            reason_parameters)


class CannotLoadRenamePlanPermissionsError(CannotLoadRenamePlanError):
    def __init__(self, filename):
        CannotLoadRenamePlanError.__init__(
            self,
            filename,
            'of a permissions issue')


class CannotLoadRenamePlanFailedReadingFileError(CannotLoadRenamePlanError):
    def __init__(self, filename):
        CannotLoadRenamePlanError.__init__(
            self,
            filename,
            "the file could not be read")


class CannotLoadRenamePlanInvalidFormatError(CannotLoadRenamePlanError):
    def __init__(self, filename):
        CannotLoadRenamePlanError.__init__(
            self,
            filename,
            "the file is corrupt or not a BAON rename plan")


class CannotLoadRenamePlanOtherError(CannotLoadRenamePlanError):
    def __init__(self, filename, error):
        CannotLoadRenamePlanError.__init__(
            self,
            filename,
            'of an unspecified error',
            {'inner_error': error})


class RenamePlanExecuteError(RenamePlanError):
    def __init__(self, reason_format_string, reason_parameters=None):
        reason_parameters = dict(reason_parameters or dict())

        RenamePlanError.__init__(
            self,
            "Failed to execute rename plan because " + reason_format_string,
            reason_parameters)


class RenamePlanExecuteFailedBecauseActionFailedError(RenamePlanExecuteError):
    def __init__(self, action_error, rollback_ok):
        if rollback_ok:
            rollback_text = \
                'The actions up to this point were rolled back and the directory is now in its original condition.'
        else:
            rollback_text = \
                'WARNING! The actions were not rolled back successfully. THe directory may now be in an inconsistent '\
                'state. Proceed with caution.'

        RenamePlanExecuteError.__init__(
            self,
            "a step failed:\n\n{action_error}\n\n" + rollback_text,
            {'action_error': action_error, 'rollback_ok': rollback_ok})


class RenamePlanExecuteFailedBecauseOtherError(RenamePlanExecuteError):
    def __init__(self, error):
        RenamePlanExecuteError.__init__(
            self,
            'of an unspecified error',
            {'inner_error': error})
