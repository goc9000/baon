#!/bin/bash

APP=baon
APP_NAME=BAON
MAIN_EXEC=src/baon.py
USR_DIR=/usr/local
INSTALL_FILES="lib/antlr3 src"

function main
{
    check_root
    check_dir

    install_files
    install_icon
    install_bin_entry
    install_desktop_entry
    install_uninstaller
    
    echo "Done installing $APP_NAME!"
}

function check_root
{
    if [ `id -u` -ne 0 ]; then
        echo "You must be root to execute this script!"
        exit 1
    fi
}

function check_dir
{
    dir=`pwd`
    if [ `basename $dir` = "install" ]; then
        cd ..
    fi
    dir=`pwd`
    if [ ! `basename $dir` = $APP ]; then
        echo "You must run this script from the $APP or 'install' directories!"
        exit 1
    fi
}

function install_files
{
    rm -rf $USR_DIR/share/$APP
    mkdir -p $USR_DIR/share/$APP
    cp --parents -r $INSTALL_FILES $USR_DIR/share/$APP

    chmod a+x $USR_DIR/share/$APP/$MAIN_EXEC
}

function install_icon
{
    cp install/app_icon.png /usr/share/pixmaps/$APP.png
}

function install_bin_entry
{
    cat <<EOT >$USR_DIR/bin/$APP
#!/usr/bin/python

import sys, subprocess

args = list(sys.argv)
args[0] = '$USR_DIR/share/$APP/$MAIN_EXEC'

subprocess.Popen(args).wait()
EOT
    chmod a+x $USR_DIR/bin/$APP
}

function install_desktop_entry
{
    cat <<EOT > $USR_DIR/share/applications/$APP.desktop
#!/usr/bin/env xdg-open

[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Exec='$USR_DIR/bin/$APP' %f
Name=$APP_NAME
Icon=/usr/share/pixmaps/$APP.png
Categories=Utility;FileTools;
MimeType=inode/directory;
EOT

    chmod a+x $USR_DIR/share/applications/$APP.desktop
}

function install_uninstaller
{
    cp install/uninstall.sh $USR_DIR/share/$APP/uninstall.sh
    chmod a+x $USR_DIR/share/$APP/uninstall.sh
}

main
