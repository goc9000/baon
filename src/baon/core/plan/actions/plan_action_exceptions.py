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


class DeleteDirectoryActionException(RenamePlanActionException):
    def __init__(self, path, reason_format_string, reason_parameters=None):
        reason_parameters = dict(reason_parameters or dict())
        reason_parameters['path'] = path

        RenamePlanActionException.__init__(
            self,
            "Cannot delete directory '{path}' because " + reason_format_string,
            reason_parameters)


class CannotDeleteDirDoesNotExistException(DeleteDirectoryActionException):
    def __init__(self, path):
        DeleteDirectoryActionException.__init__(self, path, 'it does not exist')


class CannotDeleteDirIsAFileException(DeleteDirectoryActionException):
    def __init__(self, path):
        DeleteDirectoryActionException.__init__(self, path, 'it is actually a file')


class CannotDeleteDirNoPermissionsException(DeleteDirectoryActionException):
    def __init__(self, path):
        DeleteDirectoryActionException.__init__(self, path, 'we do not have permission')


class CannotDeleteDirOtherErrorException(DeleteDirectoryActionException):
    def __init__(self, path, os_error):
        DeleteDirectoryActionException.__init__(
            self, path,
            'of a system error: {exception.strerror}',
            {'exception': os_error})


class MoveFileActionException(RenamePlanActionException):
    def __init__(self, from_path, to_path, reason_format_string, reason_parameters=None):
        reason_parameters = dict(reason_parameters or dict())
        reason_parameters['from_path'] = from_path
        reason_parameters['to_path'] = to_path

        RenamePlanActionException.__init__(
            self,
            "Cannot move file '{from_path}' because " + reason_format_string,
            reason_parameters)


class CannotMoveFileDoesNotExistException(MoveFileActionException):
    def __init__(self, from_path, to_path):
        MoveFileActionException.__init__(self, from_path, to_path, 'it does not exist')


class CannotMoveFileDestinationExistsException(MoveFileActionException):
    def __init__(self, from_path, to_path):
        MoveFileActionException.__init__(
            self, from_path, to_path,
            "the destination '{to_path}' already exists")


class CannotMoveFileNoPermissionsException(MoveFileActionException):
    def __init__(self, from_path, to_path):
        MoveFileActionException.__init__(self, from_path, to_path, 'we do not have permission')


class CannotMoveFileOtherErrorException(MoveFileActionException):
    def __init__(self, from_path, to_path, os_error):
        MoveFileActionException.__init__(
            self, from_path, to_path,
            'of a system error: {exception.strerror}',
            {'exception': os_error})
