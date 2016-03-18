BAON
====

(C) Copyright 2012-present Cristian Dinu (<goc9000@gmail.com>); Licensed under the GPLv3.


Overview
--------

*BAON* (By Any Other Name) is a mass file renamer designed to work with my personal rule syntax vaguely reminiscent of ANTLR rules.


Setup
-----

On Windows and OS X, just download the app or `.msi` installer from the *Releases* section, and install it. Or, follow the instructions in the *Building and Installing* doc.


Usage Basics
------------

First, you need to specify the directory that contains the files you want to rename, i.e. the **base path**. You can either input the path directly, click the *Browse* button to search for it using the explorer, or just drag-and-drop the directory on the application icon in the dock.

BAON will scan and list the files in the directory you provided. By default, it will not enter any sub-directories, but you can adjust this by checking the **Recursively Scan Subfolders** box, in which case BAON will find and offer for renaming all files under any subfolders of the main directory.

You can specify how you want the files to be renamed by writing a set of **rules**. Rules generally look like:

    pattern1->action1  pattern2->action2  ...

meaning the following: if a filename can be split into components that simultaneously match *pattern1*, *pattern2*, etc respectively, the file will be renamed by applying the corresponding actions to each of those components so as to obtain the new filename. For instance, the rule:

    %d->%2d  ' - '->'. '  ..->title
    
will rename a file like `3 - kaiser waltz.mp3` to `03. Kaiser Waltz.mp3`.

In this example, the `%d` pattern matches the track number, and the corresponding action `->%2d` means that it will be extended with leading zeroes so that it has 2 characters. The `' - '` pattern matches the separator that follows the track number, i.e. a dash flanked by spaces, and the action `->'. '` means that it will be replaced by a period and a space. Finally, the `..` pattern matches against the rest of the filename, which will then be passed through the transformation `->title` that adjusts its capitalization in accordance to the rules for English titles.

For details about other patterns and actions available, check out the `Full Language Reference` and `Language Summary` documents.

Note that the extension is not processed by default. Normally, the scope of the renaming is the filename itself, excluding its extension and path prefix. You can check the **Use Path** and **Use Extension** boxes if you want renaming to affect these. **A very powerful feature of BAON is that changing the path of a file will cause BAON to move files between directories and in general create and remove directories so as to recreate the directory structure reflected by the new paths**.

As you type in rules, BAON will apply them to the scanned filenames and show you what the result would be. The review display automatically highlights errors, warnings or special situations such as:

- Files that map to the same destination filename (and would thus overwrite each other)
- Destination filenames that are invalid in some way (e.g. have forbidden characters) or aesthetic problems (double/leading/trailing spaces etc.)
- Filenames that have not changed (i.e. matched no rules or were not modified by the rewrites). This is not an error, but rendering these differently helps the user.

Once you are satisfied with the result and there are no problems, you can press **OK**. BAON will formulate a plan for renaming the files (and/or modifying the directory structure) and execute it. Should an unexpected error occur in the middle of the renaming process, the actions undertaken so far will be cancelled and you will not be left with a partial state on disk. BAON also saves a temporary copy of the renaming plan in your home directory, so that it can roll back the plan even if the application or computer crashed in the middle of the renaming process.
