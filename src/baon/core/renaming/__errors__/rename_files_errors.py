# baon/core/renaming/__errors__/rename_files_errors.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from abc import ABCMeta

from baon.core.errors.BAONError import BAONError
from baon.core.errors.BAONWarning import BAONWarning


class RenameFilesError(BAONError, metaclass=ABCMeta):
    pass


class RenameFilesAbortedError(RenameFilesError):
    def _get_format_string(self):
        return "The rename operation was aborted"


class UnprintableCharacterInFilenameError(RenameFilesError):
    def __init__(self, character_code):
        super(UnprintableCharacterInFilenameError, self).__init__(character_code=character_code)

    def _get_format_string(self):
        return "Non-printable character \\u{character_code:04x} present in filename"


class EmptyFilenameError(RenameFilesError):
    def _get_format_string(self):
        return 'Filename is empty'


class OnlyDotsFilenameError(RenameFilesError):
    def _get_format_string(self):
        return 'Filename may not be . or ..'


class EmptyPathComponentError(RenameFilesError):
    def _get_format_string(self):
        return 'Path has empty component'


class OnlyDotsPathComponentError(RenameFilesError):
    def _get_format_string(self):
        return 'Path may not contain a . or .. component'


class FileCollidesWithFileError(RenameFilesError):
    def _get_format_string(self):
        return 'Collides with other file'


class FileCollidesWithDirectoryError(RenameFilesError):
    def _get_format_string(self):
        return 'Collides with directory'


class DirectoryCollidesWithFileError(RenameFilesError):
    def _get_format_string(self):
        return 'Collides with other directory'


class WouldMergeImplicitlyWithOtherFoldersError(RenameFilesError):
    def _get_format_string(self):
        return 'Would merge implicitly with other folders'


class RenameFilesWarning(BAONWarning):
    pass


class ProblematicCharacterInFilenameWarning(RenameFilesWarning):
    def __init__(self, character):
        super(ProblematicCharacterInFilenameWarning, self).__init__(character=character)

    def _get_format_string(self):
        return 'Problematic character present in filename: {character}'


class PathComponentStartsWithSpaceWarning(RenameFilesWarning):
    def __init__(self, component):
        super(PathComponentStartsWithSpaceWarning, self).__init__(component=component)

    def _get_format_string(self):
        return "Path component '{component}' starts with spaces"


class PathComponentEndsWithSpaceWarning(RenameFilesWarning):
    def __init__(self, component):
        super(PathComponentEndsWithSpaceWarning, self).__init__(component=component)

    def _get_format_string(self):
        return "Path component '{component}' ends with spaces"


class PathComponentContainsDoubleSpacesWarning(RenameFilesWarning):

    def __init__(self, component):
        super(PathComponentContainsDoubleSpacesWarning, self).__init__(component=component)

    def _get_format_string(self):
        return "Path component '{component}' contains double spaces"


class FilenameStartsWithSpaceWarning(RenameFilesWarning):
    def _get_format_string(self):
        return 'Filename starts with spaces'


class BasenameEndsWithSpaceWarning(RenameFilesWarning):
    def _get_format_string(self):
        return 'Filename contains spaces before the extension'


class FilenameContainsDoubleSpacesWarning(RenameFilesWarning):
    def _get_format_string(self):
        return 'Filename contains double spaces'


class ExtensionContainsSpacesWarning(RenameFilesWarning):
    def _get_format_string(self):
        return 'Extension contains spaces'
