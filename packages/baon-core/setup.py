from setuptools import setup, find_packages

setup(
    name='baon-core',
    version='3.0.0',
    description='Mass file renamer with ANTLR-like syntax (core)',
    author='Cristian Dinu',
    author_email='goc9000@gmail.com',
    url='https://github.com/goc9000/baon',
    license='GPL-3',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'appdirs',
        'decorator',
        'ply',
    ],
)
