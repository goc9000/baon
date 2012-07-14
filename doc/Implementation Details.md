BAON
====

(C) Copyright 2012 Cristian Dinu (<goc9000@gmail.com>); Licensed under the GPLv3.

Implementation Details
----------------------

### Matches

In order to better understand how BAON works, we will start at the fundamental entity involved in the renaming process, the *match*.

A match is, essentially, an entity that looks at incoming text and checks whether part of it (usually a prefix) fits some pattern specific to the match type. If it does, then the match is said to *succeed*, and the matched prefix is removed ("consumed") from the incoming text and stored for further processing. If the text does not fit the pattern, the match is said to *fail*, and the incoming text will be unaffected.

The part of the text that was extracted is called the *matched text* and represents a preliminary *output* for the match. Once extracted, this text is filtered through a series of *actions* attached to the match. An action simply receives the current matched text and transforms it according to an algorithm specific to the action type (which may include side effects), after which the result is passed to the next action, and so on. The output of the last action is the *final result* of the match.

Note that matches may have no actions attached, in which case they simply serve as a condition that cause no modifications to the corresponding segment of the text.

### Rules

A rule's function is simply to apply a sequence of matches to a piece of text (usually a filename). If, and only if, *all* of the matches in the sequence map succeed, the rule will output the concatenation of the matched and transformed text for each component. Otherwise, the rule will undo all modifications and return the filename unchanged.

Note that the matches might not consume all of the filename text. Any remaining incoming text will be copied unchanged to the output.

### The ruleset

The topmost entity involved in the renaming process is the *ruleset*. The ruleset is responsible for mapping every file in a list to a transfomed destination filename. It does so by independently passing each filename entry through the user-supplied list of *rules*. Every time a rule 'matches' the filename, the filename text may change according to the transformations specified in the rule. Subsequent rules will be matched against the transformed text instead of the original filename.

Unless otherwise specified, a file will be be passed through every rule in the set and transformed every time a rule matches. The final transformed text obtained after all rules have been applied will be used by the ruleset as the final result of the renaming operation for that file.
