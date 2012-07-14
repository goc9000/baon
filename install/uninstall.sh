#!/bin/bash

APP=baon
APP_NAME=BAON
USR_DIR=/usr/local

function main
{
    check_root
    check_dir

    uninstall_desktop_entry
    uninstall_bin_entry
    uninstall_icon
    uninstall_files
    
    echo "Done uninstalling $APP_NAME!"
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

function uninstall_files
{
    rm -rf $USR_DIR/share/$APP
}

function uninstall_icon
{
    rm -f /usr/share/pixmaps/$APP.png
}

function uninstall_bin_entry
{
    rm -f $USR_DIR/bin/$APP
}

function uninstall_desktop_entry
{
    rm -f $USR_DIR/share/applications/$APP.desktop
}

main
