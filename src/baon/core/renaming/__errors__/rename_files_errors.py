# baon/core/renaming/__errors__/rename_files_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.errors.BAONError import BAONError
from baon.core.errors.BAONWarning import BAONWarning


class RenameFilesError(BAONError):
    def __init__(self, format_string, error_parameters=None):
        BAONError.__init__(self, format_string, error_parameters)


class UnprintableCharacterInFilenameError(RenameFilesError):
    def __init__(self, character_code):
        RenameFilesError.__init__(
            self, "Non-printable character \\u{character_code:04x} present in filename",
            {'character_code': character_code})


class EmptyFilenameError(RenameFilesError):
    def __init__(self):
        RenameFilesError.__init__(self, "Filename is empty")


class OnlyDotsFilenameError(RenameFilesError):
    def __init__(self):
        RenameFilesError.__init__(self, "Filename may not be . or ..")


class EmptyPathComponentError(RenameFilesError):
    def __init__(self):
        RenameFilesError.__init__(self, "Path has empty component")


class OnlyDotsPathComponentError(RenameFilesError):
    def __init__(self):
        RenameFilesError.__init__(self, "Path may not contain a . or .. component")


class FileCollidesWithFileError(RenameFilesError):
    def __init__(self):
        RenameFilesError.__init__(self, "Collides with other file")


class FileCollidesWithDirectoryError(RenameFilesError):
    def __init__(self):
        RenameFilesError.__init__(self, "Collides with directory")


class DirectoryCollidesWithFileError(RenameFilesError):
    def __init__(self):
        RenameFilesError.__init__(self, "Collides with other directory")


class WouldMergeImplicitlyWithOtherFoldersError(RenameFilesError):
    def __init__(self):
        RenameFilesError.__init__(self, "Would merge implicitly with other folders")


class RenameFilesWarning(BAONWarning):
    def __init__(self, format_string, error_parameters=None):
        BAONWarning.__init__(self, format_string, error_parameters)


class ProblematicCharacterInFilenameWarning(RenameFilesWarning):
    def __init__(self, character):
        RenameFilesWarning.__init__(
            self, "Problematic character present in filename: {character}",
            {'character': character})


class PathComponentStartsWithSpaceWarning(RenameFilesWarning):
    def __init__(self, component):
        RenameFilesWarning.__init__(
            self, "Path component '{component}' starts with spaces",
            {'component': component})


class PathComponentEndsWithSpaceWarning(RenameFilesWarning):
    def __init__(self, component):
        RenameFilesWarning.__init__(
            self, "Path component '{component}' ends with spaces",
            {'component': component})


class PathComponentContainsDoubleSpacesWarning(RenameFilesWarning):
    def __init__(self, component):
        RenameFilesWarning.__init__(
            self, "Path component '{component}' contains double spaces",
            {'component': component})


class FilenameStartsWithSpaceWarning(RenameFilesWarning):
    def __init__(self):
        RenameFilesWarning.__init__(self, "Filename starts with spaces")


class BasenameEndsWithSpaceWarning(RenameFilesWarning):
    def __init__(self):
        RenameFilesWarning.__init__(self, "Filename contains spaces before the extension")


class FilenameContainsDoubleSpacesWarning(RenameFilesWarning):
    def __init__(self):
        RenameFilesWarning.__init__(self, "Filename contains double spaces")


class ExtensionContainsSpacesWarning(RenameFilesWarning):
    def __init__(self):
        RenameFilesWarning.__init__(self, "Extension contains spaces")
