# baon/core/plan/__errors__/make_rename_plan_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta, abstractmethod

from baon.core.errors.BAONError import BAONError


class MakeRenamePlanError(BAONError, metaclass=ABCMeta):
    pass


class RenamedFilesListHasErrorsError(MakeRenamePlanError):
    def _get_format_string(self):
        return "Some of the files to be renamed have errors"


class CannotCreateDestinationDirError(MakeRenamePlanError, metaclass=ABCMeta):
    def __init__(self, destination_dir, **extra_parameters):
        super().__init__(destination_dir=destination_dir, **extra_parameters)

    def _get_format_string(self):
        return "Cannot create destination directory '{destination_dir}' because " +\
               self._get_reason_format_string()

    @abstractmethod
    def _get_reason_format_string(self):
        return ''


class CannotCreateDestinationDirInaccessibleParentError(CannotCreateDestinationDirError):
    def __init__(self, destination_dir):
        super().__init__(destination_dir)

    def _get_reason_format_string(self):
        return 'the parent directory is inaccessible'


class CannotCreateDestinationDirUnexpectedNonDirParentError(CannotCreateDestinationDirError):
    def __init__(self, destination_dir):
        super().__init__(destination_dir)

    def _get_reason_format_string(self):
        return 'the parent entry is unexpectedly not a directory'


class CannotCreateDestinationDirNoReadPermissionForParentError(CannotCreateDestinationDirError):
    def __init__(self, destination_dir):
        super().__init__(destination_dir)

    def _get_reason_format_string(self):
        return 'we do not have read permission on the parent directory'


class CannotCreateDestinationDirNoTraversePermissionForParentError(CannotCreateDestinationDirError):
    def __init__(self, destination_dir):
        super().__init__(destination_dir)

    def _get_reason_format_string(self):
        return 'we do not have traverse permission on the parent directory'


class CannotCreateDestinationDirNoWritePermissionForParentError(CannotCreateDestinationDirError):
    def __init__(self, destination_dir):
        super().__init__(destination_dir)

    def _get_reason_format_string(self):
        return 'we do not have write permission on the parent directory'


class CannotCreateDestinationDirFileInTheWayWillNotMoveError(CannotCreateDestinationDirError):
    def __init__(self, destination_dir):
        super().__init__(destination_dir)

    def _get_reason_format_string(self):
        return 'a file of the same name is in the way and it is not part of the move'


class RenamedFilesListInvalidMultipleDestinationsError(MakeRenamePlanError):
    def __init__(self, source, destination_1, destination_2):
        super().__init__(source=source, destination_1=destination_1, destination_2=destination_2)

    def _get_format_string(self):
        return "Rename list is invalid: '{source}' is renamed to both '{destination_1}' and '{destination_2}'"


class RenamedFilesListInvalidSameDestinationError(MakeRenamePlanError):
    def __init__(self, destination, source_1, source_2):
        super().__init__(destination=destination, source_1=source_1, source_2=source_2)

    def _get_format_string(self):
        return "Rename list is invalid: Both '{source_1}' and '{source_2}' are renamed to '{destination}'"


class CannotMoveFileNoWritePermissionForDirError(MakeRenamePlanError):
    def __init__(self, source, destination, directory):
        super().__init__(source=source, destination=destination, directory=directory)

    def _get_format_string(self):
        return "Cannot rename '{source}' to '{destination}' as we do not have write permission on '{directory}'"
