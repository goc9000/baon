# baon/core/files/FileScanner.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.files.FileReference import FileReference
from baon.core.files.file_scanner_exceptions import BasePathDoesNotExistException, BasePathIsNotADirectoryException,\
    CannotExploreBasePathException
from baon.core.files.file_reference_exceptions import CannotExploreDirectoryException

from baon.core.utils.ReportsProgress import ReportsProgress


class FileScanner(ReportsProgress):
    recursive = None

    def __init__(self, recursive=True, on_progress=None):
        ReportsProgress.__init__(self, on_progress)
        self.recursive = recursive
    
    def scan(self, base_path):
        stats = dict(done=0, total=1)
        self._report_progress(stats['done'], stats['total'])

        if not os.path.exists(base_path):
            raise BasePathDoesNotExistException(path=base_path)
        if not os.path.isdir(base_path):
            raise BasePathIsNotADirectoryException(path=base_path)
        try:
            os.listdir(base_path)
        except OSError as e:
            raise CannotExploreBasePathException(path=base_path, inner_exception=e)

        files = []
        self._scan(base_path, u'', True, stats, files)

        return sorted(files)

    def _scan(self, base_path, relative_path, explore_dir, stats, files_accumulator):
        full_path = os.path.join(base_path, relative_path)
        problems = []

        is_link = os.path.islink(full_path)
        is_dir = os.path.isdir(full_path)

        directory_opened = False
        files_here = None
        if is_dir and not is_link and explore_dir:
            try:
                files_here = os.listdir(full_path)
                directory_opened = True
            except OSError as e:
                problems.append(CannotExploreDirectoryException(inner_exception=e))

        if directory_opened:
            stats['done'] += 1
            stats['total'] += len(files_here)
            self._report_progress(stats['done'], stats['total'])

            for name in files_here:
                self._scan(
                    base_path,
                    os.path.join(relative_path, name),
                    self.recursive,
                    stats,
                    files_accumulator
                )

            return

        files_accumulator.append(
            FileReference(
                full_path,
                relative_path,
                is_dir,
                is_link,
                problems,
            )
        )

        stats['done'] += 1
        self._report_progress(stats['done'], stats['total'])
