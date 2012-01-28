====
BAON
====

Description
-----------

BAON (By Any Other Name) is a mass file renamer specially engineered for
working with my personal ANTLR-like rule syntax.

Specification
-------------

Usage Overview
..............

The user's main input into the renaming process is a set of `rewrite rules`
somewhat similar to those used in ANTLR_. Rules generally take the form:

    `match-specification` ``->`` `rewrite-specification`

and bear the following basic semantics: if a filename matches
`match-specification`, it will be transformed according to
`rewrite-specification`.

Every file in the current rename session will be walked through all rules
specified by the user. Whenever a rule matches, the filename will be changed
accordingly and, unless otherwise specified, processing will continue with the
next rule (which will now match against the changed filename).

Once all filenames have been processed, the user will review the complete set
of transformations and confirm or deny the committal of the new filenames to
disk. The program will perform no actual modifications of the file system up to
this point.

The renaming review display will highlight special situations such as:

- Filenames that map to the same destination filename (and would thus overwrite
  each other).
- Destination filenames that are invalid in some way (e.g. have invalid
  characters)
- Filenames that have not changed (i.e. matched no rules or were not modified
  by the rewrites). This is not an error, but rendering these differently helps
  the user.

The program will not allow the user to proceed until all errors are resolved.

Once the filename remapping has been validated, the program will begin the
actual renaming of the files. This will have to be done in an intelligent
manner, as a number of issues may come into play:

- It might not be possible to directly rename all files to their final
  destination, as name clashes may occur in this intermediate state even though
  no conflicts occur in the final state, e.g. in the case of a mapping like
  `fileA` -> `fileB`, `fileB` -> `fileA`. Thus, the program will have to order
  the individual renaming operations appropriately and use temporary
  destinations where necessary.
- The program may find that a certain file cannot be renamed at the current time
  because it is in use. The entire batch of operations should be rolled back so
  as not to leave the files in an intermediate, 'inconsistent', state.
- Ideally, the program should also guard against the possiblity of a crash
  during the rename by keeping a temporary log of all operations planned and
  achieved, so that the original structure may be restored in case the program
  is interrupted during a batch rename operation.

Rules
.....

As stated before, rules have the general form:

    `matches` ``->`` `rewrites`

The purpose of the `matches` section is twofold:

- To identify the filenames to which this particular rule applies
- To identify different parts in the filenames that do match the rule, so that
  different rewriting operations can be applied to each
  
// TODO:

in matches:
%d   (digits)
%3d  (exactly 3 digits)
" arbitrary text "
*  (everything to the next match)
case:  (turns case sensitivity on from this point onwards)
alias=%d (antlr-like aliases)

<once the matches end, everything up to the 
<by default, only the base filename is processed (no extension); to cover that,
 you need a special match>

in rewrites:

%d  (interpret as number, output)
%02d  (as in printf)
*  (output as parsed)
alias  (move alias here; it is removed from the queue, we are still positioned
        over the element that would come were there no alias)
alias:%d  (same, but apply %d interpretation)
title: (and other functions; apply function 'title' (titlecaps) to all text that follows)
:title (end scope of 'title:' - kind of like a paranthesis)
!stop (and other predicates; if rule matched, do not process others for this file)
(' '->'_';'a'->'z')  (an example; upon the text in this match, execute other rules)

Matches
.......

Rewrites
........

Input Modifiers
...............

Output Modifiers
................

Special Predicates
..................

.. _ANTLR: http://www.antlr.org