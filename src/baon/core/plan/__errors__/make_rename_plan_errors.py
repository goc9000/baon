# baon/core/plan/__errors__/make_rename_plan_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONError import BAONError


class MakeRenamePlanError(BAONError):
    def __init__(self, format_string, error_parameters=None):
        BAONError.__init__(self, format_string, error_parameters)


class CannotCreateDestinationDirError(MakeRenamePlanError):
    def __init__(self, destination_dir, reason_format_string, reason_parameters=None):
        reason_parameters = dict(reason_parameters or dict())
        reason_parameters['destination_dir'] = destination_dir

        MakeRenamePlanError.__init__(
            self,
            "Cannot create destination directory '{destination_dir}' because " + reason_format_string,
            reason_parameters)


class CannotCreateDestinationDirInaccessibleParentError(CannotCreateDestinationDirError):
    def __init__(self, destination_dir):
        CannotCreateDestinationDirError.__init__(
            self,
            destination_dir,
            "the parent directory is inaccessible")


class CannotCreateDestinationDirUnexpectedNonDirParentError(CannotCreateDestinationDirError):
    def __init__(self, destination_dir):
        CannotCreateDestinationDirError.__init__(
            self,
            destination_dir,
            "the parent entry is unexpectedly not a directory")


class CannotCreateDestinationDirNoReadPermissionForParentError(CannotCreateDestinationDirError):
    def __init__(self, destination_dir):
        CannotCreateDestinationDirError.__init__(
            self,
            destination_dir,
            "we do not have read permission on the parent directory")


class CannotCreateDestinationDirNoTraversePermissionForParentError(CannotCreateDestinationDirError):
    def __init__(self, destination_dir):
        CannotCreateDestinationDirError.__init__(
            self,
            destination_dir,
            "we do not have traverse permission on the parent directory")


class CannotCreateDestinationDirNoWritePermissionForParentError(CannotCreateDestinationDirError):
    def __init__(self, destination_dir):
        CannotCreateDestinationDirError.__init__(
            self,
            destination_dir,
            "we do not have write permission on the parent directory")


class CannotCreateDestinationDirFileInTheWayWillNotMoveError(CannotCreateDestinationDirError):
    def __init__(self, destination_dir):
        CannotCreateDestinationDirError.__init__(
            self,
            destination_dir,
            "a file of the same name is in the way and it is not part of the move")


class RenamedFilesListInvalidMultipleDestinationsError(MakeRenamePlanError):
    def __init__(self, source, destination_1, destination_2):
        MakeRenamePlanError.__init__(
            self,
            "Rename list is invalid: '{source}' is renamed to both '{destination_1}' and '{destination_2}' ",
            {'source': source, 'destination_1': destination_1, 'destination_2': destination_2})


class RenamedFilesListInvalidSameDestinationError(MakeRenamePlanError):
    def __init__(self, destination, source_1, source_2):
        MakeRenamePlanError.__init__(
            self,
            "Rename list is invalid: Both '{source_1}' and '{source_2}' are renamed to '{destination}'",
            {'destination': destination, 'source_1': source_1, 'source_2': source_2})


class CannotMoveFileNoWritePermissionForDirError(MakeRenamePlanError):
    def __init__(self, source, destination, directory):
        MakeRenamePlanError.__init__(
            self,
            "Cannot rename '{source}' to '{destination}' as we do not have write permission on '{directory}'",
            {'source': source, 'destination': destination, 'directory': directory})
