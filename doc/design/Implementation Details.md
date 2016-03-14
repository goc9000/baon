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

### Matches

Within the framework set up by the *context* concept above, a **match** in the most abstract sense can be described as an entity that takes in a context and produces *zero, one, or more* resulting contexts, called **solutions**.

For instance, a simple pattern match such as `%d` will inspect the `text` and `position` attributes of the input context so as to see whether the incoming text matches its specific pattern (a number). If the pattern fits, it will produce a single solution context where the number text has been consumed and placed in the `matched_text` attribute, as illustrated here:

|                   | Text (position marked with *) | Matched Text    | Aliases      | Anchored          |
|-------------------|-------------------------------|-----------------|--------------|-------------------|
| Input context     | `The Year `* `2000`           | N/A             | Not relevant | Not relevant      |
| Solution          | `The Year 2000` *             | `2000`          | Not affected | Always set to Yes |

If the pattern does not fit, no solutions will be produced. In general, pattern matches will produce either one solution or none, depending on whether the pattern fits or not. However, composite matches may have multiple solutions. For instance, an alternatives match:

    ('abr'|%d|'a'|%s)

Applied to the text `abracadabra` will yield:

| Match                    | Text (position marked with *) | Matched Text    | Aliases      | Anchored          |
|--------------------------|-------------------------------|-----------------|--------------|-------------------|
| Input context            | * `abracadabra`               | N/A             | Not relevant | Not relevant      |
| Solution 1 (for `'abr'`) | `abr` * `acadabra`            | `abr`           | Not affected | Always set to Yes |
| Solution 2 (for `'a'`)   | `a` * `bracadabra`            | `a`             | Not affected | Always set to Yes |
| Solution 3 (for `%s`)    | `abracadabra` *               | `abracadabra`   | Not affected | Always set to Yes |

Note how a solution is produced for every alternative that matches the incoming text.

Optional and repeated matches also produce multiple solutions in order to implement their backtracking semantics. For instance, `abc*` applied to the text `abcabcabcabc` yields:

| Match                    | Text (position marked with *) | Matched Text    | Aliases      | Anchored          |
|--------------------------|-------------------------------|-----------------|--------------|-------------------|
| Input context            | * `abcabcabcabc`              | N/A             | Not relevant | Not relevant      |
| Solution 1               | `abcabcabcabc` *              | `abcabcabcabc`  | Not affected | Yes               |
| Solution 2               | `abcabcabc` * `abc`           | `abcabcabc`     | Not affected | Yes               |
| Solution 3               | `abcabc` * `abcabc`           | `abcabc`        | Not affected | Yes               |
| Solution 4               | `abc` * `abcabcabc`           | `abc`           | Not affected | Yes               |
| Solution 5               | * `abcabcabcabc`              | (empty text)    | Not affected | Not affected      |

Note that the *order of the solutions* is important, and in fact determines which variant BAON will try first. As one can see, the variants with the most repetitions will be tried first, then, if this does not succeed, fewer and fewer repetitions will be attempted, until either the global match is successful, or the repeated match is skipped entirely.

### Taxonomy of Matches

Matches can be roughly categorized as follows:

- **Material matches**: Material matches are those that depend on the content of the incoming text and/or the position within it. Thus, they consult and modify the `text` and `position` fields, and may succeed or fail depending on whether the text matches their programmed pattern. They behave closest to what would be intuitively thought of as a match.
  - **Pattern matches**: Depend on the content of the incoming text, regardless of position.
    - *Literal text matches*
    - Most *format matches*: `%d`, `%s`, `%c`, `%parens` etc.
  - **Positional matches**: Depend on the position in the filename text.
    - The *anchor matches*: `^` and `$`
  - **Mixed pattern/positional matches**: Depend on both the content and the position.
    - `%inparens`, `%inbraces`, `%incurlies`
    - *Regular expression matches* (positional features like lookahead/behind etc. work as expected)

  Notes:
  - The `anchored` field of the context will always be set to `true` following the success of a material match.
  - Currently, all pattern and positional matches translate to an equivalent regex in the backend.

- **Immaterial matches**: Immaterial matches do not depend on the content of or position in the incoming text in order to succeed. They always execute, consume no text, and do not limit the expansion of constructs such as `..`.
  - **Insertions**: Insertions basically just set the `matched_text` field directly to whatever needs to be inserted (literal text or the contents of an alias)
  - *The search-and-replace match*: Technically this does affect the incoming text, but in a different, out-of-band fashion with respect to the normal streaming paradigm of matching. The position is also always unchanged. Only text past the current position is affected.
  
  Notes:
  - The `position` and `anchored` fields of the context are guaranteed to be unchanged following an immaterial match.
  - The search-and-replace match is technically also a *composite* match (see below).

- **Composite matches**: Composite matches are objects that contain other matches (simple or themselves composite) and execute them in an organized way, or change their functioning.
  - *Match sequences*
  - *Match alternatives*
  - *Optional matches*
  - *Repeated matches*
  - *Matches with actions*
  
  Notes:
  - Optional and repeated matches are actually the same object. In fact, the object supports full regex-like counting semantics for minimum and maximum repetitions, but this functionality is not fully exposed in the syntax. Instead, we have the `?`, `*`, `+` operators which map to (min=0, max=1), (min=0, max=Inf) and (min=1, max=Inf) respectively.
  - Composite matches behave like a material or immaterial match depending on the matches they contain and the circumstances of the execution (i.e. the currently selected alternative, whether an optional match was skipped, etc.).
  - Match groups are not mentioned because they only exist on a syntactic level. In the AST they are present as sequence, alternative, actioned, etc. matches.

- **Special matches**: Currently this contains only one entry:
  - *The 'between' match*: Neither material, immaterial, nor composite. This is the match that actually makes use of the `anchored` flag and the only one that can set it to false. Consult the dedicated section for details.

### Actions

The subject of **actions** consists of two main parts:
- What the actions themselves are
- How actions are integrated with matches

Like matches, actions also do a mapping from one context to another, but with two important differences:
- Actions operate on a reduced kind of context called an **action context**, which consists of only two fields: `text` and `aliases`. These are loaded from the `matched_text` and `aliases` fields of the match context, and stored back when actions have finished executing. Thus, *actions cannot consult or influence the incoming text*, and only act on the matched text produced by the match to be last executed.
- Actions always have exactly one "solution", which is to say that they always succeed in transforming the text and always transform it in only one way, specific to their nature.

The following table illustrates the effects of various actions given a starting action context:

|                      | Text          | Aliases            |
|----------------------|---------------|--------------------|
| Input action context | `brown fox`   | -                  |
| `!`                  | (empty text)  | -                  |
| `->upper`            | `BROWN FOX`   | -                  |
| `->braces`           | `[BROWN FOX]` | -                  |
| `>>phrase`           | `brown fox`   | phrase=`brown fox` |
| `->(%s>>word %s!)`   | `brown`       | word=`brown`       |

It should be noted that matches, as defined previously, have no concept of actions. The way actions are integrated into the match framework is through the use of a special composite match type called **MatchWithActions**. A match object of this type stores a core match and a list of actions, and makes them act like a single, actionless match from the outside. The algorithm is simple: the solutions produced by the MatchWithActions object are all of the solutions of the core match, transformed by passing their `matched_text` and `aliases` fields through all the stored actions.


-------------

REWRITE POINT

-------------

### Rules

A rule's function is simply to apply a sequence of matches to a piece of text (usually a filename). If, and only if, *all* of the matches in the sequence map succeed, the rule will output the concatenation of the matched and transformed text for each component. Otherwise, the rule will undo all modifications and return the filename unchanged.

Note that the matches might not consume all of the filename text. Any remaining incoming text will be copied unchanged to the output.

### The ruleset

The topmost entity involved in the renaming process is the *ruleset*. The ruleset is responsible for mapping every file in a list to a transfomed destination filename. It does so by independently passing each filename entry through the user-supplied list of *rules*. Every time a rule 'matches' the filename, the filename text may change according to the transformations specified in the rule. Subsequent rules will be matched against the transformed text instead of the original filename.

Unless otherwise specified, a file will be be passed through every rule in the set and transformed every time a rule matches. The final transformed text obtained after all rules have been applied will be used by the ruleset as the final result of the renaming operation for that file.
