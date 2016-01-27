#!/usr/bin/env python3

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys


PIP = 'pip3'
PYTHON = 'python3'

DIST_DIR = 'dist'

CORE_PKG = 'baon-core'


memo_pip_installed = None
memo_pkg_installed = dict()


def fail(format_str, *args, **kwargs):
    print(format_str.format(*args, **kwargs), file=sys.stderr)
    sys.exit(-1)


def recon_ui_packages():
    if not os.path.isdir(os.path.join('packages', CORE_PKG)):
        fail('ERROR: this script must be run from the project root dir')

    return [
        entry for entry in os.listdir('packages')
        if entry != CORE_PKG and os.path.isdir(os.path.join('packages', entry))
    ]


def silent_call(*args, **kwargs):
    return subprocess.call(*args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kwargs) == 0


def check_pip_installed():
    global memo_pip_installed

    if memo_pip_installed is not None:
        return memo_pip_installed

    try:
        silent_call(PIP)
        memo_pip_installed = True
    except:
        memo_pip_installed = False

    return memo_pip_installed


def ensure_pip_installed():
    if not check_pip_installed():
        fail('ERROR: {0} is not installed, fix this and retry', PIP)


def check_package_installed(package):
    global memo_pkg_installed

    ensure_pip_installed()

    memo_val = memo_pkg_installed.get(package)
    if memo_val is not None:
        return memo_val

    memo_val = silent_call([PIP, 'show', package])

    memo_pkg_installed[package] = memo_val

    return memo_val


def install_package(package, from_url=None):
    global memo_pkg_installed

    ensure_pip_installed()

    if from_url is None:
        print('Installing package: {0}'.format(package))
        silent_call([PIP, 'install', package])
    else:
        print('Installing package: {0} from {1}'.format(package, from_url))
        silent_call([PIP, 'install', from_url])

    memo_pkg_installed[package] = True


def ensure_package_installed(package):
    if not check_package_installed(package):
        install_package(package)


def uninstall_package(package):
    global memo_pkg_installed

    print('Uninstalling package: {0}'.format(package))
    ensure_pip_installed()
    silent_call([PIP, 'uninstall', '-y', package])
    memo_pkg_installed[package] = False


def ensure_package_uninstalled(package):
    if check_package_installed(package):
        uninstall_package(package)


def build_wheels(packages):
    for package in packages:
        build_wheel(package)


def build_wheel(package):
    ensure_package_installed('wheel')

    print('Building wheel for package: {0}'.format(package))

    package_dir = os.path.join('packages', package)

    silent_call(
        [PYTHON, 'setup.py', 'bdist_wheel', '-d', os.path.join('..', '..', DIST_DIR)],
        cwd=package_dir,
    )

    # Cleanup
    shutil.rmtree(os.path.join(package_dir, 'build'))
    egg_info_dir = glob.glob(os.path.join(package_dir, 'src', '*.egg-info'))
    if len(egg_info_dir) > 0:
        shutil.rmtree(egg_info_dir[0])


def install_app_packages(packages):
    for package in packages:
        install_package(package, from_url=os.path.join('packages', package))


def uninstall_app_packages(packages):
    for package in packages:
        ensure_package_uninstalled(package)


def main():
    known_uis = recon_ui_packages()

    parser = argparse.ArgumentParser(description='Make script for BAON')

    parser.add_argument('--ui-packages', default=','.join(known_uis), metavar='<ui1,ui2,...>',
                        help='Override list of UI packages to install/build')

    subparsers = parser.add_subparsers(title='commands', dest='command')
    subparsers.add_parser('build', help='Build .whl packages for the core and GUIs')
    subparsers.add_parser('install', help='(Re)Install BAON in package form')
    subparsers.add_parser('uninstall', help='Uninstall BAON packages')

    raw_args = parser.parse_args(sys.argv[1:])

    if raw_args.command is None:
        parser.print_usage()
        return

    uis = [ui_spec.strip() for ui_spec in re.split(',', raw_args.ui_packages) if ui_spec.strip() != '']
    for ui in uis:
        if ui not in known_uis:
            parser.error("No package for UI '{0}'".format(ui))
    packages = [CORE_PKG] + uis

    if raw_args.command == 'build':
        build_wheels(packages)
    elif raw_args.command == 'install':
        build_wheels(packages)
        uninstall_app_packages(packages)
        install_app_packages(packages)
    elif raw_args.command == 'uninstall':
        uninstall_app_packages(packages)


main()