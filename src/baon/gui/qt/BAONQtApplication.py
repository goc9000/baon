# baon/gui/qt/BAONQtApplication.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import sys

from PyQt4.QtGui import QApplication


class BAONQtApplication(QApplication):
    def __init__(self, args):
        QApplication.__init__(self, sys.argv)
