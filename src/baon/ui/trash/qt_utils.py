# baon/gui/qt_utils.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


def qstr_to_unicode(qstring):
    return unicode(qstring.toUtf8(), 'utf-8')
