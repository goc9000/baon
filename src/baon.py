#!/usr/bin/python3

# baon.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.app_args import parse_app_args

from baon.ui.qt_gui.BAONQtApplication import BAONQtApplication


if __name__ == "__main__":
    args = parse_app_args()

    BAONQtApplication(args).exec_()
