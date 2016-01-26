from distutils.core import setup
from setuptools import find_packages

setup(
    name='baon-gui-qt4',
    version='3.0.0',
    description='Mass file renamer with ANTLR-like syntax (QT4 GUI)',
    author='Cristian Dinu',
    author_email='goc9000@gmail.com',
    url='https://github.com/goc9000/baon',
    license='GPL-3',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'baon-core',
    ],
)
