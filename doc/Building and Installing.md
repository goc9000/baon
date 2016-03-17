BAON
====

(C) Copyright 2012-present Cristian Dinu (<goc9000@gmail.com>); Licensed under the GPLv3.


Building and Installing
=======================


Requirements
------------

First and foremost, building and running BAON requires **Python 3.3** or later.

The following Python packages are required for the BAON core:
- `appdirs`
- `decorator`
- `ply`

These extra packages are also required for building full deployments of BAON:
- `py2app` (for building an OS X app)
- `cx-Freeze` and `pypiwin32` (for building a Windows app)

The QT4 GUI also requires:
- QT 4.8 or later (but not QT5)
- The `PyQt4` Python package

All of these except for `PyQt4` can be installed using `pip`. Note that the full deployments come with all requirements built in, and otherwise most of these packages do not need to be installed manually: BAON packages built using the make script automatically install the runtime dependencies, and the make script also automatically installs any build requirements.


Building
--------

Use the `make.py` script in the root directory (make sure it's run with Python 3) to generate the following kinds of deployments for BAON:

- An OS X app (use `make.py build_app`)
- A Windows app (use `make.py build_exe`)
- A Windows app installer (use `make.py build_msi`)
- Python packages in the wheel format (use `make.py build`). Separate packages will be created for the core and each UI.

There is no build command for a Linux deployment yet. Linux users can install the wheel packages and then write a script to invoke BAON using a command like `python3 -m baon`.


Installing
----------

The app deployments of BAON can be installed with the standard methods on that system (dragging an app to the `Applications` folder on OS X, running the installer or copying it to `Program Files` on Windows).

Once built, the Python wheel packages can be installed using:

    make.py install

They will then be available to the local Python installation and can be run with a command like:

    python3 -m baon
