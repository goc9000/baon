====
BAON
====

Description
-----------

BAON (By Any Other Name) is a mass file renamer specially engineered for
working with my personal rule syntax vaguely reminiscent of ANTLR rewrite rules.

Specification
-------------

Usage Overview
..............

The user's main input into the renaming process is a set of `renaming rules`.
Rules generally take the form:

    *pattern-1* *action-1* *pattern-2* *action-2* ... *pattern-N* *action-N*

and bear the following basic semantics: if a file's name can be split into
components that simultaneously match *pattern-1*, *pattern-2*, ... *pattern-N*
respectively, the file will be renamed by applying the corresponding actions
to each of those components so as to obtain the new filename. For instance,
the rule::

    %d->%02d ' - '->'. ' ..->title
    
will rename a file like::

    3 - kaiser waltz.mp3

to::

    03. Kaiser Waltz.mp3

The ``%d`` matches against the number track number and the corresponding
transformation implies rendering the number in two digit format with leading
zeroes. The ``' - '`` specifier matches against that exact character sequence,
which will then be replaced by the exact text ``'. '``. Finally, the ``..``
specifier matches against the rest of the filename, which will then be passed
through the transformation ``title`` that renders the matched text in title
caps. Note that the extension is not processed by default.

Unless otherwise specified, a file will be be passed through every rule in the
set and transformed every time a rule matches. After a match and transformation,
subsequent rules will be matched against the transformed text (not the original
filename).

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
  no conflicts occur in the final state, e.g. in the case of a mapping like::

   fileA -> fileB
   fileB -> fileA

  Thus, the program will have to order
  the individual renaming operations appropriately and use temporary
  destinations where necessary.
- The program may find that a certain file cannot be renamed at the current time
  because it is in use. The entire batch of operations should be rolled back so
  as not to leave the files in an intermediate, 'inconsistent', state.
- Ideally, the program should also guard against the possibility of a crash
  during the rename by keeping a temporary log of all operations planned and
  achieved, so that the original structure may be restored in case the program
  is interrupted during a batch rename operation.

Regular Match Specifiers
........................

BAON supports the following set of match specifiers:

``%d``
    Matches a **positive, integral** number.

``%Nd``
    Matches a positive, integral number consisting of exactly *N* digits.

``%s``
    Matches the first contiguous sequence of characters delimited by whitespace
    (just like its ``scanf`` counterpart). Note that any leading whitespace is
    forgotten (it will be consumed, but not appear as part of the matched text).

``%Ns``
    As above, except only the first *N* characters of the string are matched and
    consumed.

``%c``
    Matches a single character at the current position, including whitespace.
    Note that this always succeeds, unless we are at the end of the scope.

``%Nc``
    As above, but matches exactly *N* characters.

``%ws``
    Matches any amount of whitespace (even none) at this position.

``'exact-text'`` or ``"exact-text"``
    Matches the exact text between the (double) quotes. All the well-known
    backslash-based escape sequences may be used.

``/regular-expression/``
    Matches the regular expression between the slashes. You must use the Python
    flavor of regular expressions, despite the JavaScript-like delimiters. You
    may specify flags by adding any of the following characters immediately
    after the ending slash:
   
    - ``i``: case insensitivity

``..``
    Matches everything up to the point where the next specifier matches, i.e.
    if the next specifier is ``%d``, this matches everything up to the next
    number. It is an error to have two consecutive specifiers of this type.

``$``
    Matches the end of the current scope. The default scope is the entire
    filename save for the extension.

``(rule)``
    Matches the pattern defined by a sub-rule. The sub-rule may itself contain
    actions that transform the components as they are matched. The content of
    the match will consist of the entire text matched by the sub-rule after all
    of the transformations therein have been applied.

``+``
    States that the previous match will be repeated as many times as possible.
    Actions may be placed both between the pattern and this sign, in which case
    they apply to each occurrence individually, or after the sign, in which case
    they apply to the totality of text that spans all occurrences.

``*``
    Like above, but allows for the possibility of there being no first match at
    all, i.e. it matches 0 or more successive occurrences of the pattern.

``?``
    States that the previous match is optional, i.e. matches 0 or one occurrence
    of the pattern.

Insertion Match Specifiers
..........................

``<<'exact-text'``
    Matches and consumes no text, but inserts the exact text specified at the
    current position.

``<<alias``
    Consumes no text, but inserts the text stored under the given alias at the
    current position. The text is available for further transformation by
    actions appearing after this match specifier. It is permissible for the
    initial association of the alias to occur at a later point in the rule.

Special Predicate Specifiers
............................

Predicate specifiers consume and match no text.

``#ext``
    Extends the scope of the search to cover the entire filename (by default,
    the extension is excluded from the scope). This only applies for the current
    rule. If present, this predicate must appear at the beginning of the rule,
    before any regular match specifier.

``#stop``
    If the filename matched the rule, stops any further processing for this
    filename after all transformations have been applied. If present, this must
    appear at the very end of the rule.

Search-and-replace Match Specifiers
...................................

``@``

Actions
.......

Multiple actions may appear after a match specifier, the semantics being that
the text is passed through each corresponding transformation in turn, and the
end result is pasted into the destination filename.

*(null)*
    If a match is not followed by any action specification, the default action
    is to render the matched text unmodified. Note that for some types of
    matches, this might not coincide with the original text in the filename.

``!``
    Deletes the matched text.

``->%0Nd``
    Interprets the matched text as a positive, integral number and renders it
    using an *N*-digit format featuring leading zeroes. An error will be
    reported if the matched text is not a number.

``->fail``
    Declares a failed match for this rule (or sub-rule) and continues with the
    next rule in the set. This is useful for adding exceptions to a rule,
    especially in combination with the ``?`` specifier.

``->title``
    Renders the matched text in title case (first letter of every word
    capitalized). Some prepositions such as 'a', 'an', 'on', etc. are not
    capitalized unless they occur at the very beginning of the matched text.

``->upper``
    Renders the matched text in upper case.

``->lower``
    Renders the matched text in lower case.

``->(rule)``
    Applies an arbitrary sub-rule to the matched text.

``>>alias``
    Deletes the text and stores it under the given alias. The token can then be
    pasted at other places in the destination filename using the ``<<`` 
    specifier.
