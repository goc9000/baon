# baon/core/plan/actions/__errors__/plan_action_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONError import BAONError


class RenamePlanActionError(BAONError):
    def __init__(self, format_string, error_parameters=None):
        BAONError.__init__(self, format_string, error_parameters)


class CreateDirectoryActionError(RenamePlanActionError):
    def __init__(self, path, reason_format_string, reason_parameters=None):
        reason_parameters = dict(reason_parameters or dict())
        reason_parameters['path'] = path

        RenamePlanActionError.__init__(
            self,
            "Cannot create directory '{path}' because " + reason_format_string,
            reason_parameters)


class CannotCreateDirAlreadyExistsError(CreateDirectoryActionError):
    def __init__(self, path):
        CreateDirectoryActionError.__init__(self, path, 'it already exists')


class CannotCreateDirFileInWayError(CreateDirectoryActionError):
    def __init__(self, path):
        CreateDirectoryActionError.__init__(self, path, 'a file by that name already exists')


class CannotCreateDirParentDoesNotExistError(CreateDirectoryActionError):
    def __init__(self, path):
        CreateDirectoryActionError.__init__(self, path, 'the parent directory does not exist')


class CannotCreateDirParentNotADirectoryError(CreateDirectoryActionError):
    def __init__(self, path):
        CreateDirectoryActionError.__init__(self, path, 'the parent entry is not a directory')


class CannotCreateDirNoPermissionsError(CreateDirectoryActionError):
    def __init__(self, path):
        CreateDirectoryActionError.__init__(self, path, 'we do not have permission')


class CannotCreateDirOtherError(CreateDirectoryActionError):
    def __init__(self, path, os_error):
        CreateDirectoryActionError.__init__(
            self, path,
            'of a system error: {error.strerror}',
            {'error': os_error})


class DeleteDirectoryActionError(RenamePlanActionError):
    def __init__(self, path, reason_format_string, reason_parameters=None):
        reason_parameters = dict(reason_parameters or dict())
        reason_parameters['path'] = path

        RenamePlanActionError.__init__(
            self,
            "Cannot delete directory '{path}' because " + reason_format_string,
            reason_parameters)


class CannotDeleteDirDoesNotExistError(DeleteDirectoryActionError):
    def __init__(self, path):
        DeleteDirectoryActionError.__init__(self, path, 'it does not exist')


class CannotDeleteDirIsAFileError(DeleteDirectoryActionError):
    def __init__(self, path):
        DeleteDirectoryActionError.__init__(self, path, 'it is actually a file')


class CannotDeleteDirNoPermissionsError(DeleteDirectoryActionError):
    def __init__(self, path):
        DeleteDirectoryActionError.__init__(self, path, 'we do not have permission')


class CannotDeleteDirOtherError(DeleteDirectoryActionError):
    def __init__(self, path, os_error):
        DeleteDirectoryActionError.__init__(
            self, path,
            'of a system error: {error.strerror}',
            {'error': os_error})


class MoveFileActionError(RenamePlanActionError):
    def __init__(self, from_path, to_path, reason_format_string, reason_parameters=None):
        reason_parameters = dict(reason_parameters or dict())
        reason_parameters['from_path'] = from_path
        reason_parameters['to_path'] = to_path

        RenamePlanActionError.__init__(
            self,
            "Cannot move file '{from_path}' because " + reason_format_string,
            reason_parameters)


class CannotMoveFileDoesNotExistError(MoveFileActionError):
    def __init__(self, from_path, to_path):
        MoveFileActionError.__init__(self, from_path, to_path, 'it does not exist')


class CannotMoveFileDestinationExistsError(MoveFileActionError):
    def __init__(self, from_path, to_path):
        MoveFileActionError.__init__(
            self, from_path, to_path,
            "the destination '{to_path}' already exists")


class CannotMoveFileNoPermissionsError(MoveFileActionError):
    def __init__(self, from_path, to_path):
        MoveFileActionError.__init__(self, from_path, to_path, 'we do not have permission')


class CannotMoveFileOtherError(MoveFileActionError):
    def __init__(self, from_path, to_path, os_error):
        MoveFileActionError.__init__(
            self, from_path, to_path,
            'of a system error: {error.strerror}',
            {'error': os_error})
