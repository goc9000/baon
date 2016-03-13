BAON
====

(C) Copyright 2012-present Cristian Dinu (<goc9000@gmail.com>); Licensed under the GPLv3.


-------------------

REWRITE IN PROGRESS

-------------------


Implementation Details
======================


The Text Matching and Transformation Model
------------------------------------------

### Contexts

The first fundamental concept that underlies the matching engine is the **context**. A context is a description of the situation at any time during the matching and transformation process, and consists of the following attributes:

- `text`: The complete filename text that is to be parsed and potentially transformed. Usually this is constant throughout the match process, but may be changed by a search-and-replace match.
- `position`: The position, within the above text, at which we are currently looking for a match. This starts from 0 and advances as we consume more of the text.
- `aliases`: All the saved aliases and their content.
- `matched_text`: The text matched and/or transformed by the match that was last processed.
- `anchored`: A flag that affects the behavior of the 'between' match. Basically, the context becomes unanchored following a 'between' match, and becomes anchored again after a *material* match, i.e. one that depends on the content of or position in the incoming text (as opposed to things like insertions or search-and-replace matches, which can apply anywhere in the text).

For instance, given the following input filename:

    1. overture

And the rule:

    %d->%2d>>trackno ". " @"o"->"ou" ..->title

The evolution of the context will be as follows:

| Moment                        | Text (position marked with *) | Matched Text    | Aliases      | Anchored |
|-------------------------------|-------------------------------|-----------------|--------------|----------|
| Beginning of processing       | * `1. overture`               | N/A             | -            | Yes      |
| `%d` processed                | `1` * `. overture`            | `1`             | -            | Yes      |
| `->%2d` action processed      | `1` * `. overture`            | `01`            | -            | Yes      |
| `>>trackno` action processed  | `1` * `. overture`            | `01`            | trackno=`01` | Yes      |
| `". "` processed              | `1._` * `overture`            | `._`            | trackno=`01` | Yes      |
| `@"o"->"ou"` processed        | `1._` * `ouverture`           | N/A             | trackno=`01` | Yes      |
| `..` processed                | `1. ouverture` *              | `ouverture`     | trackno=`01` | No       |
| `->title` action processed    | `1. ouverture` *              | `Ouverture`     | trackno=`01` | No       |
| Match sequence processed      | `1. ouverture` *              | `01. Ouverture` | trackno=`01` | No       |
| Processing complete           | `1. ouverture` *              | `01. Ouverture` | trackno=`01` | No       |

### Matches (preliminary)

Within the framework set up by the *context* concept above, a **match** can be preliminarily described as an entity that takes in a context, and, if the right conditions are met (i.e. it fits a pattern), produces another context, called a **solution**. In maths parlance, a match can be said to be a *partial function* from C to C, where C is the set of all possible contexts.

For instance, a simple pattern match such as `%d` will inspect the `text` and `position` attributes of the input context so as to see whether the incoming text matches its specific pattern (a number). If the pattern fits, it will produce a solution context where the number text has been consumed and placed in the `matched_text` attribute, as illustrated here:

|                   | Text (position marked with *) | Matched Text    | Aliases      | Anchored          |
|-------------------|-------------------------------|-----------------|--------------|-------------------|
| Input context     | `The Year `* `2000`           | N/A             | Not relevant | Not relevant      |
| Solution          | `The Year 2000` *             | `2000`          | Not affected | Always set to Yes |

Note that this definition is actually incomplete, but it covers the most fundamental pattern and positional matches from which more complex matches are formed. A complete definition will be given in a subsequent section, after actions are also introduced.

### Actions

Similarly to matches, **actions** also take in a context and produce a resulting context. However, unlike matches, actions only inspect and affect the `matched_text` and `aliases` attributes, as they are designed to act upon the result of a previously executed match.

Here is an illustration of an input context (following a match) and the resulting contexts following the execution of various actions:

|                    | Text (position marked with *) | Matched Text  | Aliases            | Anchored     |
|--------------------|-------------------------------|---------------|--------------------|--------------|
| Input context      | `The quick brown fox` *       | `brown fox`   | -                  | Not relevant |
| `!`                | Not affected                  | (empty text)  | -                  | Not affected |
| `->upper`          | Not affected                  | `BROWN FOX`   | -                  | Not affected |
| `->braces`         | Not affected                  | `[BROWN FOX]` | -                  | Not affected |
| `>>phrase`         | Not affected                  | `brown fox`   | phrase=`brown fox` | Not affected |
| `->(%s>>word %s!)` | Not affected                  | `brown`       | word=`brown`       | Not affected |

### Insertions

**Insertions** are simply "matches" that produce a `matched_text` regardless of the current `text` and `position` attributes, which are neither consulted nor affected.

For instance, here is an illustration of an input context before and after some possible insertions:

|                    | Text (position marked with *) | Matched Text  | Aliases      | Anchored     |
|--------------------|-------------------------------|---------------|--------------|--------------|
| Input context      | Not relevant                  | N/A           | word=`quick` | Not relevant |
| `<<"brown fox"`    | Not affected                  | `brown fox `  | word=`quick` | Not affected |
| `<<word`           | Not affected                  | `quick`       | word=`quick` | Not affected |

Insertions are *immaterial*, in that they never cause the `anchored` attribute to revert to `true`. This is the main difference between them and the almost equivalent construct `''->'brown fox'`.

-------------

REWRITE POINT

-------------


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
