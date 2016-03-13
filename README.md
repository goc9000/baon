BAON
====

(C) Copyright 2012-present Cristian Dinu (<goc9000@gmail.com>); Licensed under the GPLv3.


-------------------

REWRITE IN PROGRESS

-------------------


Overview
--------

BAON (By Any Other Name) is a mass file renamer designed to work with my personal rule syntax vaguely reminiscent of ANTLR rules.

Setup
-----

BAON requires Python, Qt4 with Python bindings, and the PLY Python package. To compile everything, simply use `make`. To install BAON in `/usr/local`, use `make install`.

Usage Basics
------------

The user can specify how he wants the files to be renamed by writing a set of *rules*. Rules generally look like:

    pattern1->action1  pattern2->action2  ...

meaning the following: if a filename can be split into components that simultaneously match *pattern1*, *pattern2*, etc respectively, the file will be renamed by applying the corresponding actions to each of those components so as to obtain the new filename. For instance, the rule:

    %d->%02d  ' - '->'. '  ..->title
    
will rename a file like `3 - kaiser waltz.mp3` to `03. Kaiser Waltz.mp3`.

In this example, the `%d` pattern matches against the track number, and the corresponding transformation implies rendering the number in two digit format with leading zeroes. The `' - '` pattern matches against that exact character sequence, which will then be replaced by the exact text `'. '`. Finally, the `..` pattern matches against the rest of the filename, which will then be passed through the transformation `title` that renders the matched text in title caps.

For details about other patterns and actions available, check out the `Full Language Reference` document. You can also read the `Implementation Details` document for a better understanding of how BAON works behind the scenes.

Note that the extension is not processed by default. Normally, the scope of the renaming is the filename itself, excluding its extension and path prefix. The user may activate options so as to extend the scope to these components as well. Modifying the path component of the filename will cause the file to be moved to another directory.

Once all filenames have been processed, the user can review the complete set of transformations and confirm or cancel the rename operation. The review display automatically highlights errors, warnings or special situations such as:

- Files that map to the same destination filename (and would thus overwrite each other).
- Destination filenames that are invalid in some way (e.g. have forbidden characters) or aesthetic problems (double/leading/trailing spaces etc.)
- Filenames that have not changed (i.e. matched no rules or were not modified by the rewrites). This is not an error, but rendering these differently helps the user.

The program will not allow the user to proceed until all errors are resolved.

Renaming is done according to a plan with undoable actions, so that if an error occurs in the middle of the renaming process, the actions undertaken so far will be cancelled and you will not be left with a partial state on disk. BAON also saves a temporary copy of the renaming plan in your home directory, so that it can roll back the plan even if the application or computer crashed in the middle of the renaming process.
