BAON
====

(C) Copyright 2012-present Cristian Dinu (<goc9000@gmail.com>); Licensed under the GPLv3.


Strengths and Limitations
=========================


Strengths
---------

- Powerful and expressive language:
  - Transformations are inline with the matching (i.e. `match1->action1` instead of `match1` and `action1` in two separate fields, requiring one to remember the association)
  - Powerful constructs like the 'between' match or the search-and-replace match
  - Backtracking (most other matchers are greedy)

- Paths can be manipulated just as easily as filenames, BAON will figure out the required directory structure transformations
- High resistance to unexpected errors: plans will be rolled back if an operation fails, and backups will be saved to allow revert even if the program crashes


Limitations
-----------

- Not designed to handle operations across filesystems with different rules
- Not tested on FAT or exotic filesystems
- Links are not followed or handled (they are treated like an opaque file)
- Only rudimentary support for permissions on Windows. Some situations where we are missing the required permissions will only be detected during the execution of the plan.
