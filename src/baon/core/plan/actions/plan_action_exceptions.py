# baon/core/plan/actions/plan_actions_exceptions.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONExceptionBase import BAONExceptionBase


class RenamePlanActionException(BAONExceptionBase):
    def __init__(self, format_string, error_parameters=None):
        BAONExceptionBase.__init__(self, format_string, error_parameters)


class CreateDirectoryActionException(RenamePlanActionException):
    def __init__(self, path, reason_format_string, reason_parameters=None):
        reason_parameters = dict(reason_parameters or dict())
        reason_parameters['path'] = path

        RenamePlanActionException.__init__(
            self,
            "Cannot create directory '{path}' because " + reason_format_string,
            reason_parameters)


class CannotCreateDirAlreadyExistsException(CreateDirectoryActionException):
    def __init__(self, path):
        CreateDirectoryActionException.__init__(self, path, 'it already exists')


class CannotCreateDirFileInWayException(CreateDirectoryActionException):
    def __init__(self, path):
        CreateDirectoryActionException.__init__(self, path, 'a file by that name already exists')


class CannotCreateDirParentDoesNotExistException(CreateDirectoryActionException):
    def __init__(self, path):
        CreateDirectoryActionException.__init__(self, path, 'the parent directory does not exist')


class CannotCreateDirParentNotADirectoryException(CreateDirectoryActionException):
    def __init__(self, path):
        CreateDirectoryActionException.__init__(self, path, 'the parent entry is not a directory')


class CannotCreateDirNoPermissionsException(CreateDirectoryActionException):
    def __init__(self, path):
        CreateDirectoryActionException.__init__(self, path, 'we do not have permission')


class CannotCreateDirOtherErrorException(CreateDirectoryActionException):
    def __init__(self, path, os_error):
        CreateDirectoryActionException.__init__(
            self, path,
            'of a system error: {exception.strerror}',
            {'exception': os_error})
