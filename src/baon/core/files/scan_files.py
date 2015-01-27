# baon/core/files/scan_files.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from collections import deque

from baon.core.files.baon_paths import extend_path
from baon.core.files.FileReference import FileReference
from baon.core.files.scan_files_exceptions import BasePathDoesNotExistException, BasePathIsNotADirectoryException,\
    CannotExploreBasePathException
from baon.core.files.file_reference_exceptions import CannotExploreDirectoryException


def _dummy_on_progress(done, total):
    pass


def scan_files(base_path, recursive=True, on_progress=_dummy_on_progress):
    done = 0
    total = 1
    on_progress(done, total)

    if not os.path.exists(base_path):
        raise BasePathDoesNotExistException(path=base_path)
    if not os.path.isdir(base_path):
        raise BasePathIsNotADirectoryException(path=base_path)
    try:
        os.listdir(base_path)
    except OSError as e:
        raise CannotExploreBasePathException(path=base_path, inner_exception=e)

    scan_queue = deque([''])
    files = []

    while len(scan_queue) > 0:
        relative_path = scan_queue.popleft()
        full_path = os.path.join(base_path, relative_path)

        problems = []

        is_link = os.path.islink(full_path)
        is_dir = os.path.isdir(full_path)

        directory_opened = False
        if is_dir and not is_link and (recursive or relative_path == ''):
            try:
                files_in_dir = os.listdir(full_path)
                scan_queue.extend(extend_path(relative_path, name) for name in files_in_dir)
                total += len(files_in_dir)
                directory_opened = True
            except OSError as e:
                problems.append(CannotExploreDirectoryException(inner_exception=e))

        if not directory_opened:
            files.append(
                FileReference(
                    full_path,
                    relative_path,
                    is_dir,
                    is_link,
                    problems,
                )
            )

        done += 1
        on_progress(done, total)

    return sorted(files)
