# baon/core/plan/actions/__errors__/plan_action_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta, abstractmethod

from baon.core.errors.BAONError import BAONError


class RenamePlanActionError(BAONError, metaclass=ABCMeta):
    pass


class CreateDirectoryActionError(RenamePlanActionError, metaclass=ABCMeta):
    def __init__(self, path, **extra_parameters):
        super().__init__(path=path, **extra_parameters)

    def _get_format_string(self):
        return "Cannot create directory '{path}' because " + self._get_reason_format_string()

    @abstractmethod
    def _get_reason_format_string(self):
        return ''


class CannotCreateDirAlreadyExistsError(CreateDirectoryActionError):
    def __init__(self, path):
        super().__init__(path)

    def _get_reason_format_string(self):
        return 'it already exists'


class CannotCreateDirFileInWayError(CreateDirectoryActionError):
    def __init__(self, path):
        super().__init__(path)

    def _get_reason_format_string(self):
        return 'a file by that name already exists'


class CannotCreateDirParentDoesNotExistError(CreateDirectoryActionError):
    def __init__(self, path):
        super().__init__(path)

    def _get_reason_format_string(self):
        return 'the parent directory does not exist'


class CannotCreateDirParentNotADirectoryError(CreateDirectoryActionError):
    def __init__(self, path):
        super().__init__(path)

    def _get_reason_format_string(self):
        return 'the parent entry is not a directory'


class CannotCreateDirNoPermissionsError(CreateDirectoryActionError):
    def __init__(self, path):
        super().__init__(path)

    def _get_reason_format_string(self):
        return 'we do not have permission'


class CannotCreateDirOtherError(CreateDirectoryActionError):
    def __init__(self, path, os_error):
        super().__init__(path, os_error=os_error)

    def _get_reason_format_string(self):
        return 'of a system error: {error.strerror}'


class DeleteDirectoryActionError(RenamePlanActionError, metaclass=ABCMeta):
    def __init__(self, path, **extra_parameters):
        super().__init__(path=path, **extra_parameters)

    def _get_format_string(self):
        return "Cannot delete directory '{path}' because " + self._get_reason_format_string()

    @abstractmethod
    def _get_reason_format_string(self):
        return ''


class CannotDeleteDirDoesNotExistError(DeleteDirectoryActionError):
    def __init__(self, path):
        super().__init__(path)

    def _get_reason_format_string(self):
        return 'it does not exist'


class CannotDeleteDirIsAFileError(DeleteDirectoryActionError):
    def __init__(self, path):
        super().__init__(path)

    def _get_reason_format_string(self):
        return 'it is actually a file'


class CannotDeleteDirNoPermissionsError(DeleteDirectoryActionError):
    def __init__(self, path):
        super().__init__(path)

    def _get_reason_format_string(self):
        return 'we do not have permission'


class CannotDeleteDirNotEmptyError(DeleteDirectoryActionError):
    def __init__(self, path):
        super().__init__(path)

    def _get_reason_format_string(self):
        return 'it is unexpectedly not empty'


class CannotDeleteDirOtherError(DeleteDirectoryActionError):
    def __init__(self, path, os_error):
        super().__init__(path, os_error=os_error)

    def _get_reason_format_string(self):
        return 'of a system error: {error.strerror}'


class MoveFileActionError(RenamePlanActionError, metaclass=ABCMeta):
    def __init__(self, from_path, to_path, **extra_parameters):
        super().__init__(from_path=from_path, to_path=to_path, **extra_parameters)

    def _get_format_string(self):
        return "Cannot move file '{from_path}' because " + self._get_reason_format_string()

    @abstractmethod
    def _get_reason_format_string(self):
        return ''


class CannotMoveFileDoesNotExistError(MoveFileActionError):
    def __init__(self, from_path, to_path):
        super().__init__(from_path, to_path)

    def _get_reason_format_string(self):
        return 'it does not exist'


class CannotMoveFileDestinationExistsError(MoveFileActionError):
    def __init__(self, from_path, to_path):
        super().__init__(from_path, to_path)

    def _get_reason_format_string(self):
        return "the destination '{to_path}' already exists"


class CannotMoveFileNoPermissionsError(MoveFileActionError):
    def __init__(self, from_path, to_path):
        super().__init__(from_path, to_path)

    def _get_reason_format_string(self):
        return 'we do not have permission'


class CannotMoveFileOtherError(MoveFileActionError):
    def __init__(self, from_path, to_path, os_error):
        super().__init__(from_path, to_path, os_error=os_error)

    def _get_reason_format_string(self):
        return 'of a system error: {error.strerror}'
