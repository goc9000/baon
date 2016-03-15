BAON
====

(C) Copyright 2012-present Cristian Dinu (<goc9000@gmail.com>); Licensed under the GPLv3.


Design Decisions
================


Table of Contents
-----------------

1. [Why an ANTLR-like matching language?] (#why-an-antlr-like-matching-language)
2. [Why support backtracking?] (#why-support-backtracking)
3. [Why a staging-directory-based rename plan algorithm?] (#why-a-staging-directory-based-rename-plan-algorithm)
4. [Why use platform-specific path separators inside BAON?] (#why-use-platform-specific-path-separators-inside-baon)
5. [Why Python?] (#why-python)
6. [Why Python 3?] (#why-python-3)
7. [Why QT?] (#why-qt)
8. [Why support for multiple UIs?] (#why-support-for-multiple-uis)
9. [Why use PLY for parsing?] (#why-use-ply-for-parsing)


Why an ANTLR-like matching language?
------------------------------------

- It's just what I find most natural
- Strikes a balance between expressivity and power (language is definitely far more powerful than regexes)
- Several killer features vs. most other ad-hoc languages used in renamers:
  - The 'between' match
  - Backtracking (most other matchers are greedy)
  - Transformations are inline with the matching (i.e. `match1->action1 `instead of `match1` and `action1` in two separate fields, requiring one to remember the association)


Why support backtracking?
-------------------------

- Needed to produce an intuitive result for patterns such as `%d %d? %d` versus the text `1 2`.
- Filenames are relatively short (rarely more than several hundred chars)
- The full exponential cost is not trivial to produce by accident. For most practical patterns, the complexity is more like polynomial.
- Could be optimized via memoization if need be

Why a staging-directory-based rename plan algorithm?
----------------------------------------------------

- I tried the alternative: efficiently create only the required destination directories, move files directly whenever possible, "nudge" files otherwise (i.e. rename them temporarily so they are out of the way), delete directories that are left empty.
  - Found there are too many obscure corner cases caused by the compounding of factors such as:
    - Some filesystems are case insensitive, so an entry like `abc` also blocks `AbC`, `abC`, etc.
    - Also these may do a no-op for a rename like `abc`->`aBC` when done in-place
    - We may want to rename a directory in the middle of a path, i.e. `/abc/def/ghi/jkl` to `/abc/xyz/ghi/jkl`
    - Worse, some directories may merge or split as a result of a rename
    - Permissions
  - Renames and mk/rmdirs are very cheap, the vastly increased code complexity and bugginess is not justified

- Briefly considered another alternative based on a full AI planning algorithm as described in the theory (with preconditions, postconditions, actions, facts etc.). Would be able to be efficient in terms of the operations produced, and also corner cases would be automatically figured out by the AI.
  - Would be too expensive at evaluation time (BAON might be run on structures with 10,000s of files)
  - Again, overkill for this application


Why use platform-specific path separators inside BAON?
------------------------------------------------------

- The alternative would be a uniform path separator like `/`, even when run on Windows.

- Uniform:
  - Advantage: Rules would work the same on all platforms
  - Disadvantage: There would be a dissonance between paths as they are input in the "Base Path" field (or as program arguments), and how they appear in the files list (and thus presented to the rename rules). No matter where we make the conversion, it will look weird and cause confusion.
  - Disadvantage: Although `/` is also forbidden in NTFS, it is not portable to assume that `/` will definitely not be a part of any path component name under any possible filesystem

- Platform-specific:
  - Disavantage: Rules have to be changed on Windows (to replace `/` with `\`)
    - Counter: Rules are generally throwaway jobs, it's not a very frequent use case to save them and re-apply them on a different platform
    - Counter: Explicit path references are not used so often, usually it's simpler to just use `..`
  - Disadvantage: If `\` is a frequently used character, it has to always be quoted inside string literals (BAON previously used C-style quoting in string literals, including support for Unicode escapes).
    - Counter: Actually, there is no need to support C-style escapes. Tabs and control characters are forbidden anyway, and it's not a good idea to use Unicode characters that you can't type in filenames. Switched to Excel-style quoting.
  - Advantage: Consonance between how paths look in BAON and how they look in the operating system
  - Advantage: Fewer assumptions are made about the underlying filesystem

- Based on the above, decided for platform-specific separators


Why Python?
-----------

- Excellent support for lambdas and generators, which are crucial to the match engine. The multiple solutions of a match MUST be evaluated lazily, recursively and in a very specific order, and Python generators are perfect for elegantly expressing this.
- Rejected C#: Probably powerful enough, but has poor traction outside Windows.
- Rejected Java: Strong typing and comes with Swing built-in, which I know to be very good for this job. However, poor/no support for generators. Also packaging it with the application is problematic due to its large size vs. Python.
- Rejected Haskell: Definitely has excellent expressivity, but the UI support is relatively poor.


Why Python 3?
-------------

- Main reason is improved and more uniform Unicode support. I had lots of problems with forgotten encodes/decodes in obscure places.


Why QT?
-------

- Actually not a strong decision, there is support for multiple UIs
- I know it well
- The signal/slot mechanism is very handy in creating a non-blocking UI
- Disappointed with `wxWidgets`, found it to be crash-prone on Unices


Why support for multiple UIs?
-----------------------------

- I find I need it often in the command line, I have plans for `ncurses` or `readline` UIs.
- QT is overkill, and support might be harder in the future
- A very good exercise in separating the core vs the UI


Why use PLY for parsing?
------------------------

- Is fairly simple and well-integrated with Python idioms
- First version of BAON actually used ANTLR - this was removed as it was a very heavy Java dependency and integration with Python was poor and buggy
- BAON is not a particularly complex language, could also write a parser by hand for it
