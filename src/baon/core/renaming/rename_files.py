# baon/core/renaming/rename_files.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import re
import os

from collections import defaultdict

from baon.core.files.baon_paths import all_path_components, all_partial_paths, extend_path, split_path_and_filename

from baon.core.renaming.RenamedFileReference import RenamedFileReference
from baon.core.renaming.rename_files_exceptions import UnprintableCharacterInFilenameException, EmptyFilenameException,\
    OnlyDotsFilenameException, EmptyPathComponentException, OnlyDotsPathComponentException,\
    FileCollidesWithFileException, FileCollidesWithDirectoryException, DirectoryCollidesWithFileException,\
    WouldMergeImplicitlyWithOtherFoldersException, ProblematicCharacterInFilenameWarning,\
    PathComponentStartsWithSpaceWarning, PathComponentEndsWithSpaceWarning, PathComponentContainsDoubleSpacesWarning,\
    FilenameStartsWithSpaceWarning, BasenameEndsWithSpaceWarning, FilenameContainsDoubleSpacesWarning,\
    ExtensionContainsSpacesWarning


NON_PRINTABLE_REGEX = re.compile(ur'[\u0000-\u001f]')
PROBLEM_CHARS_REGEX = re.compile(r'["*:<>?\\/]')
ONLY_DOTS_REGEX = re.compile(ur'^[.]+$')


def _dummy_on_progress(done, total):
    pass


def rename_files(files, rule_set, use_path=False, use_extension=False, overrides=None, on_progress=_dummy_on_progress):
    done = 0
    total = len(files)
    on_progress(done, total)

    renamed_files = []

    for file_ref in files:
        renamed_files.append(
            _rename_file(file_ref, rule_set, use_path=use_path, use_extension=use_extension, overrides=overrides)
        )
        done += 1
        on_progress(done, total)

    _verify_renamed_files(renamed_files)

    return renamed_files


def _rename_file(file_ref, rule_set, use_path=False, use_extension=False, overrides=None):
    full_filename = file_ref.filename
    problems = []

    if (overrides is not None) and (full_filename in overrides):
        return RenamedFileReference(file_ref, overrides[full_filename], is_override=True)

    try:
        full_filename = _get_renamed_filename(full_filename, rule_set, use_path=use_path, use_extension=use_extension)
    except Exception as e:
        problems.append(e)

    return RenamedFileReference(file_ref, full_filename, problems=problems)


def _get_renamed_filename(full_filename, rule_set, use_path, use_extension):
    input_text = full_filename
    path = u''
    extension = u''

    if not use_path:
        path, input_text = split_path_and_filename(input_text)
    if not use_extension:
        input_text, extension = os.path.splitext(input_text)

    rename_result = rule_set.apply_on(input_text)
    output_text = rename_result.text

    if not use_extension:
        output_text += extension
    if not use_path:
        output_text = extend_path(path, output_text)

    return output_text


def _verify_renamed_files(renamed_files):
    """
    Performs verifications.

    Note: by design, the renamer will only perform verifications that do
    not require further accesses to the filesystem. Errors that can only be
    detected by using such information will be caught in the planning phase.
    """

    for renamed_fref in renamed_files:
        _check_for_intrinsic_errors(renamed_fref)
        _check_for_intrinsic_warnings(renamed_fref)

    _check_for_collisions(renamed_files)


def _check_for_intrinsic_errors(renamed_fref):
    full_filename = renamed_fref.filename
    problems = renamed_fref.problems

    m = NON_PRINTABLE_REGEX.search(full_filename)
    if m is not None:
        problems.append(UnprintableCharacterInFilenameException(ord(m.group(0))))

    path_components = all_path_components(full_filename)
    path_components, filename = path_components[:-1], path_components[-1]

    if filename == u'':
        problems.append(EmptyFilenameException())
    if ONLY_DOTS_REGEX.match(filename):
        problems.append(OnlyDotsFilenameException())
    if any(component == u'' for component in path_components):
        problems.append(EmptyPathComponentException())
    if any(ONLY_DOTS_REGEX.match(component) for component in path_components):
        problems.append(OnlyDotsPathComponentException())


def _check_for_intrinsic_warnings(renamed_fref):
    full_filename = renamed_fref.filename
    problems = renamed_fref.problems

    path_components = all_path_components(full_filename)

    m = PROBLEM_CHARS_REGEX.search(u''.join(path_components))
    if m is not None:
        problems.append(ProblematicCharacterInFilenameWarning(character=m.group(0)))

    path_components, filename = path_components[:-1], path_components[-1]

    for component in path_components:
        if component.startswith(u' '):
            problems.append(PathComponentStartsWithSpaceWarning(component=component))
        if component.endswith(u' '):
            problems.append(PathComponentEndsWithSpaceWarning(component=component))
        if u'  ' in component:
            problems.append(PathComponentContainsDoubleSpacesWarning(component=component))

    basename, extension = os.path.splitext(filename)

    if basename.startswith(u' '):
        problems.append(FilenameStartsWithSpaceWarning())
    if basename.endswith(u' '):
        problems.append(BasenameEndsWithSpaceWarning())
    if u'  ' in basename:
        problems.append(FilenameContainsDoubleSpacesWarning())
    if u' ' in extension:
        problems.append(ExtensionContainsSpacesWarning())


def _check_for_collisions(renamed_files):
    file_path_use_counts = defaultdict(int)
    dir_path_use_counts = defaultdict(int)
    partial_dir_paths = set()

    for f in renamed_files:
        if f.is_dir:
            dir_path_use_counts[f.filename] += 1
        else:
            file_path_use_counts[f.filename] += 1

        for path in all_partial_paths(f.filename)[:-1]:
            partial_dir_paths.add(path)

    for f in renamed_files:
        if f.is_dir:
            if file_path_use_counts[f.filename] > 0:
                f.problems.append(DirectoryCollidesWithFileException())
            elif (dir_path_use_counts[f.filename] > 1) or (f.filename in partial_dir_paths):
                f.problems.append(WouldMergeImplicitlyWithOtherFoldersException())
        else:
            if file_path_use_counts[f.filename] > 1:
                f.problems.append(FileCollidesWithFileException())
            elif (dir_path_use_counts[f.filename] > 0) or (f.filename in partial_dir_paths) or \
                    (f.filename in partial_dir_paths):
                f.problems.append(FileCollidesWithDirectoryException())