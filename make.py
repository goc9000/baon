#!/usr/bin/env python

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

from functools import lru_cache


DIST_DIR = 'dist'
CORE_PKG = 'baon-core'

APP_METADATA = None
PIP = None
PYTHON = None


def fail(format_str, *args, **kwargs):
    print(format_str.format(*args, **kwargs), file=sys.stderr)
    sys.exit(-1)


def recon_python3():
    global PYTHON

    if check_program_installed('python3'):
        PYTHON = 'python3'
        return

    PYTHON = 'python'
    ensure_program_installed('python')

    version = subprocess.check_output([PYTHON, '-V'], stderr=subprocess.STDOUT)

    assert not version.startswith(b'2.'), 'This script requires Python 3 to be accessible via the command line'


def recon_pip():
    global PIP

    if check_program_installed('pip3'):
        PIP = 'pip3'
        return

    PIP = 'pip'
    ensure_program_installed('pip')

    version = subprocess.check_output([PIP, '-V'], stderr=subprocess.STDOUT)

    assert b'ython 2' not in version, 'This script requires PIP for Python 3 to be accessible via the command line'


def silent_call(program_args, *args, **kwargs):
    ensure_program_installed(program_args[0])

    return subprocess.call(program_args, *args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kwargs) == 0


@lru_cache()
def check_program_installed(program):
    return shutil.which(program) is not None


def ensure_program_installed(program):
    if not check_program_installed(program):
        fail('ERROR: {0} is not installed, fix this and retry', program)


@lru_cache()
def check_package_installed(package):
    return silent_call([PIP, 'show', package])


def install_package(package, from_url=None):
    if from_url is None:
        print('Installing package: {0}'.format(package))
        silent_call([PIP, 'install', package])
    else:
        print('Installing package: {0} from {1}'.format(package, from_url))
        silent_call([PIP, 'install', from_url])

    check_package_installed.cache_clear()


def ensure_package_installed(package):
    if not check_package_installed(package):
        install_package(package)


def uninstall_package(package):
    print('Uninstalling package: {0}'.format(package))
    silent_call([PIP, 'uninstall', '-y', package])

    check_package_installed.cache_clear()


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


def clean_source():
    silent_call(['find', 'packages', '-name', '*.pyc', '-delete'])
    silent_call(['find', 'packages', '-name', '__pycache__', '-delete'])


def compile_qt4_resources():
    with tempfile.TemporaryDirectory() as work_dir:
        shutil.copy(os.path.join('resources', 'app_icon.png'), os.path.join(work_dir, 'app_icon.png'))

        with open(os.path.join(work_dir, 'resources.qrc'), 'w') as f:
            f.write("\n".join([
                '<!DOCTYPE RCC>',
                '<RCC version="1.0">',
                '  <qresource>',
                '    <file>app_icon.png</file>',
                '  </qresource>',
                '</RCC>',
            ]))

        silent_call([
            'pyrcc4',
            '-no-compress',
            '-py3',
            os.path.join(work_dir, 'resources.qrc'),
            '-o',
            os.path.join('packages', 'baon-gui-qt4', 'src', 'baon', 'ui', 'qt4_gui', 'resources.py'),
        ])


def build_osx_app(packages):
    ensure_package_installed('py2app')

    with tempfile.TemporaryDirectory() as work_dir:
        write_sources_blob(work_dir, packages, ['baon', 'baon.ui'])

        includes_option = get_ui_modules(packages)
        if 'baon-gui-qt4' in packages:
            includes_option.append('sip')

        # This package needs to be included as-is because ply uses inspect on its source, so the .pyc files are not
        # sufficient.
        packages_option = ['baon.core.parsing']

        with open(os.path.join(work_dir, 'setup.py'), 'w') as f:
            f.write("\n".join([
                "from setuptools import setup",
                "",
                "setup(",
                "    app=[{0}],".format(repr(write_start_script(work_dir))),
                "    options={'py2app': dict(",
                "        argv_emulation=True,",
                "        iconfile={0},".format(repr(build_osx_icns(work_dir))),
                "        includes={0},".format(repr(includes_option)),
                "        packages={0},".format(repr(packages_option)),
                "        plist={0},".format(repr(get_plist())),
                "    )},",
                "    setup_requires=['py2app'],",
                ")",
            ]))

        silent_call([PYTHON, 'setup.py', 'py2app'], cwd=work_dir)

        if not os.path.isdir(DIST_DIR):
            os.mkdir(DIST_DIR)

        final_app_dir = os.path.join(DIST_DIR, '{0}.app'.format(APP_METADATA.APP_NAME))
        if os.path.isdir(final_app_dir):
            shutil.rmtree(final_app_dir)

        os.rename(
            os.path.join(work_dir, 'dist', '{0}.app'.format(APP_METADATA.APP_NAME)),
            final_app_dir,
        )


def get_ui_modules(packages):
    """
    Returns a list of all UI modules corresponding to the specified packages. This list is often necessary because
    BAON imports UIs dynamically, so py2app and cx_freeze will not detect them.
    """
    modules = []
    for package in packages:
        package_ui_path = os.path.join('packages', package, 'src', 'baon', 'ui')
        for module in os.listdir(package_ui_path):
            if os.path.isdir(os.path.join(package_ui_path, module)):
                modules.append('baon.ui.' + module)

    return modules


def write_sources_blob(work_dir, packages, namespace_packages):
    """
    Merge all the code in one local blob and add __init__.py files where necessary. This needs to be done because
    neither py2app nor cx_freeze handle namespace packages well.
    """
    for package in packages:
        silent_call(['cp', '-r', os.path.join('packages', package, 'src', 'baon'), work_dir])

    for package in namespace_packages:
        with open(os.path.join(work_dir, package.replace('.', os.path.sep), '__init__.py'), 'w') as f:
            f.write('')


def write_start_script(work_dir):
    script_name = 'start_baon.py'

    with open(os.path.join(work_dir, script_name), 'w') as f:
        f.write("\n".join([
            'from baon.start import start_baon',
            '',
            'start_baon()',
        ]))

    return script_name


def build_osx_icns(work_dir):
    iconset_dir = os.path.join(work_dir, '{0}.iconset'.format(APP_METADATA.APP_NAME))
    icon_name = '{0}.icns'.format(APP_METADATA.APP_NAME)

    os.mkdir(iconset_dir)

    for size in [16, 32, 64, 128, 256, 512]:
        for retina in [False, True]:
            silent_call([
                'sips',
                '-z',
                str((size * 2) if retina else size),
                str((size * 2) if retina else size),
                os.path.join('resources', 'app_icon.png'),
                '--out',
                os.path.join(iconset_dir, 'icon_{0}x{0}{1}.png'.format(size, '@2x' if retina else '')),
            ])

    silent_call(['iconutil', '-c', 'icns', iconset_dir, '-o', os.path.join(work_dir, icon_name)])

    shutil.rmtree(iconset_dir)

    return icon_name


def get_plist():
    return dict(
        CFBundleDisplayName=APP_METADATA.APP_NAME,
        CFBundleName=APP_METADATA.APP_NAME,

        CFBundleIdentifier='com.goc9000.osx.baon',
        CFBundleVersion=APP_METADATA.APP_VERSION,
        CFBundleShortVersionString=shorten_version(APP_METADATA.APP_VERSION),
        LSApplicationCategoryType='public.app-category.utilities',

        CFBundleDocumentTypes=[
            dict(
                CFBundleTypeName='Folder',
                CFBundleTypeOSTypes=['fold'],
                CFBundleTypeRole='Viewer',
            ),
        ],

        CFBundleGetInfoString=APP_METADATA.APP_DESCRIPTION,
        NSHumanReadableCopyright=APP_METADATA.APP_COPYRIGHT,
    )


def shorten_version(version):
    return '.'.join(version.split('.')[:2])


def ensure_correct_cwd():
    if not os.path.isdir(os.path.join('packages', CORE_PKG)):
        fail('ERROR: this script must be run from the project root dir')


def load_app_metadata():
    global APP_METADATA

    sys.path.append(os.path.join('packages', CORE_PKG, 'src', 'baon'))
    APP_METADATA = __import__('app_metadata')


def recon_ui_packages():
    return [
        entry for entry in os.listdir('packages')
        if entry != CORE_PKG and os.path.isdir(os.path.join('packages', entry))
    ]


def main():
    ensure_correct_cwd()
    load_app_metadata()
    known_uis = recon_ui_packages()

    app_name = APP_METADATA.APP_NAME

    recon_python3()
    recon_pip()

    parser = argparse.ArgumentParser(description='Make script for {0}'.format(app_name))

    parser.add_argument('--ui-packages', default=','.join(known_uis), metavar='<ui1,ui2,...>',
                        help='Override list of UI packages to install/build')

    subparsers = parser.add_subparsers(title='commands', dest='command')

    # HAX: sabotage prefix_chars to disable recognition of option arguments
    sp = subparsers.add_parser('run', help='Run {0} directly from source'.format(app_name), prefix_chars='\0')
    sp.add_argument('run_args', nargs=argparse.REMAINDER, help='Program arguments')

    subparsers.add_parser('build', help='Build .whl packages for the core and GUIs')
    subparsers.add_parser('build_app', help='Build OS X app')
    subparsers.add_parser('install', help='(Re)Install {0} in package form'.format(app_name))
    subparsers.add_parser('uninstall', help='Uninstall {0} packages'.format(app_name))

    subparsers.add_parser('clean_src', help='Clean source folders (remove .pyc files etc)')

    subparsers.add_parser('compile_qt4_res', help='Compile QT4 GUI resources')

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
    elif raw_args.command == 'build_app':
        build_osx_app(packages)
    elif raw_args.command == 'install':
        build_wheels(packages)
        uninstall_app_packages(packages)
        install_app_packages(packages)
    elif raw_args.command == 'uninstall':
        uninstall_app_packages(packages)
    elif raw_args.command == 'run':
        subprocess.call([PYTHON, '-m', 'baon'] + raw_args.run_args, env=dict(
            os.environ,
            PYTHONPATH=os.pathsep.join(['packages/baon-core/src', 'packages/baon-gui-qt4/src']),
        ))
    elif raw_args.command == 'clean_src':
        clean_source()
    elif raw_args.command == 'compile_qt4_res':
        compile_qt4_resources()

main()
