# baon/core/files/FileScanner.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import os

from baon.core.files.FileReference import FileReference
from baon.core.utils.ReportsProgress import ReportsProgress


class FileScanner(ReportsProgress):
    recursive = None

    def __init__(self, recursive=True, on_progress=None):
        ReportsProgress.__init__(self, on_progress)
        self.recursive = recursive
    
    def scan(self, base_path):
        if not os.path.exists(base_path):
            raise RuntimeError(u"Path '{0}' does not exist".format(base_path))
        if not os.path.isdir(base_path):
            raise RuntimeError(u"'{0}' is not a directory".format(base_path))
        
        stats = dict(done=0, total=1)
        files = []

        self._scan(base_path, u'', stats, files)

        return files

    def _scan(self, base_path, relative_path, stats, files_accumulator):
        self._report_progress(stats['done'], stats['total'])

        path = os.path.join(base_path, relative_path)

        files_here = []
        for name in os.listdir(path):
            real_path = os.path.join(path, name)
            relative_file_path = os.path.join(relative_path, name)
            files_here.append(self._scan_single_file(real_path, relative_file_path))

        files_here = sorted(files_here)

        stats['done'] += 1
        stats['total'] += len(files_here)
        self._report_progress(stats['done'], stats['total'])

        for file_ref in files_here:
            recurse = self.recursive and (file_ref.is_dir and not file_ref.is_link)

            if recurse:
                self._scan(base_path, file_ref.filename, stats, files_accumulator)
            else:
                files_accumulator.append(file_ref)
                stats['done'] += 1
                self._report_progress(stats['done'], stats['total'])

    def _scan_single_file(self, real_path, name):
        is_link = os.path.islink(real_path)
        is_dir = os.path.isdir(real_path)

        return FileReference(
            real_path,
            name,
            is_dir,
            is_link,
        )
