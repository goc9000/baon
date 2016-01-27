import os
from setuptools import setup, find_packages


def find_packages_v2(base_dir, namespace_packages=None):
    result = find_packages(base_dir)
    for np in (namespace_packages or []):
        result.append(np)
        result.extend(np + '.' + p for p in find_packages(os.path.join(base_dir, np.replace('.', os.path.sep))))

    return result


setup(
    name='baon-core',
    version='3.0.0',
    description='Mass file renamer with ANTLR-like syntax (core)',
    author='Cristian Dinu',
    author_email='goc9000@gmail.com',
    url='https://github.com/goc9000/baon',
    license='GPL-3',
    package_dir={'': 'src'},
    packages=find_packages_v2('src', namespace_packages=['baon', 'baon.ui']),
    install_requires=[
        'appdirs',
        'decorator',
        'ply',
    ],
)
