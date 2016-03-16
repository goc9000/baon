BAON
====

(C) Copyright 2012-present Cristian Dinu (<goc9000@gmail.com>); Licensed under the GPLv3.


Implementation Details
======================


Table of Contents
-----------------

1. [The Text Matching and Transformation Model] (#the-text-matching-and-transformation-model)
  1. [Contexts] (#contexts)
  2. [Matches] (#matches)
  3. [Taxonomy of Matches] (#taxonomy-of-matches)
  4. [Actions] (#actions)
  5. [How the 'Between' Match Works] (#how-the-between-match-works)
  6. [How Rules Work] (#how-rules-work)
2. [The Rename Plan] (#the-rename-plan)


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

### How the 'Between' Match Works

The 'between' match has a complex behavior and yet a very simple implementation:
- If the `anchored` flag is `true`, we will produce solutions that cover, in order, 0, 1, 2, 3 etc. characters from the incoming text, regardless of its content. These solutions will also have the `anchored` flag set to `false`.
- Otherwise, we will produce a single solution consisting of the empty text. The `anchored` flag remains `false`.

To see why this will cause the 'between' match to ultimately span up to the first material match, let us consider what happens depending on which kind of match is executed after the 'between' match:

- *Composite match*: regardless of whether this is an alternative, sequence, etc., ultimately we will come to evaluating one of the simple matches inside (material or immaterial) at the `position` to which the 'between' match spans. The problem is restated for this match.
- *Immaterial match*: the match will execute, but by definition, `position` will not be affected. The problem is restated for the match that follows.
- *Another 'between' match*: by definition, this will always resolve to the empty text. The `position` will stay the same, and the problem is restated for the match that follows.
- *Material match*: by now it should be clear that this match will always be evaluated at the `position` to which the 'between' match spans. Then:
  - If the match is successful, then indeed the 'between' match spans to the first material match, Q.E.D.
  - If the match is not successful, BAON will backtrack and eventually try the next, longer solution for the 'between' match. The problem is restated for this longer match and an incremented `position`, until the material match is successful.
  - If we exhaust all solutions for the 'between' match (i.e. it covers the entire remaining text) without the material match being successful, the 'between' match fails, thereby transmitting the failure upstream. This again makes sense.

An interesting situation arises when *there is no next match*, i.e. the `..` is the last thing in the rule. By the algorithm previously described, one would expect that this last `..` would always be empty, because there is no next match to place any constraint on its ending position, so the first solution (0 characters) will always be chosen. And yet, what happens is what would be intuitively expected, which is that this last `..` will indeed extend until it covers the entire remaining text. To see why this is the case, consult the next section on how rules operate.

### How Rules Work

A **rule** is an abstract object that wraps a match and directs its execution against a complete filename (we say 'a match' and not 'a number of matches' because any combination of matches ultimately resolves to one composite master match, usually a sequence match). Essentially a rule solves three problems:

- A rule operates on *text* (i.e. it maps from an input filename to a transformed filename), whereas the master match operates on *match contexts*. Thus, when presented with a filename, the rule will create an initial context corresponding to that input (i.e. `text` set to the filename, `position` to 0, and `anchored` to `true`), run the master match against it, and finally extract the transformed filename from the `matched_text` field of the first found solution.

- A rule needs to transform the entire filename text, but the master match may only cover part of it. There is also the problem of `..` matches placed at the end. We elegantly solve these problems with a little trick: instead of running the master_match, we will actually run a sequence match consisting of the following three terms:

  `master_match .. $`

  We can see that:
  - If the `master_match` covers only part of the text, the extra `..` will cover the rest of the text until the `$` (the end of the filename).
  - If the `master_match` ends with a `..`, then the extra `..` will be forced to zero length, and we will immediately match against `$`, the end of the filename. The final `..` in the master match will thus grow until it extends to the end of the filename.

- Finally, there is the question of aliases being referred to before they are set (or even more complex dependencies like aliases feeding into other aliases). A rule solves this problem in the following manner: if running the match resulted in any change in the aliases, the matching will be repeated, this time with the aliases already set. The process will repeat itself until either the aliases have converged to a stable set, or we exceed a certain number of iterations. For instance, given the rule:

  `<<alias2->upper (<<alias1 <<'def')>>alias2 'abc'>>alias1`
  
  applied to the text `abc`, we will go through the following steps:
  
  | Initial `alias1` | Initial `alias2` | Final text        | Final `alias1` | Final `alias2` |
  |------------------|------------------|-------------------|----------------|----------------|
  | (empty)          | (empty)          | `defabc`          | `abc`          | `def`          |
  | `abc`            | `def`            | `DEFabcdefabc`    | `abc`          | `abcdef`       |
  | `abc`            | `abcdef`         | `ABCDEFabcdefabc` | `abc`          | `abcdef`       |

  The final text is obtained after 3 iterations, when the aliases have stabilized.


The Rename Plan
---------------

As BAON does more than just move files - it also restructures directories -, the sequence of operations to be executed can be quite complex, and as such a *rename plan* must be made.

The plan is assembled based on a list of abstract renamings, i.e. pairs of the old filename path vs the new filename path. BAON will figure out which directories should be created or removed, as well as which files should be moved and when. The result will be a sequence of three kinds of operations:

- Moving a file (or a directory)
- Creating a directory
- Removing an empty directory

The plan is assembled in 6 stages:

1. First, a temporary **staging directory** is created in the *base directory* (where the files were scanned for renaming). The name of this directory will always be picked such that it does not conflict with any other entry in the base directory. Naturally, write access for the base directory is required. Then, *create directory* operations are issued such that the final desired directory structure is recreated within the staging directory. This provides temporary destinations for all the files that are to be moved.

2. *Move file* operations are issued for all files that are to be moved or renamed. The files will be moved from their original position to a path within the staging directory that mirrors their desired final path in the staging directory.

3. *Remove directory* operations are issued for all directories that will have been left empty by the above move. These operations are orchestrated recursively from leaf to root. Note how this means that the old directory structure will be torn down except where it contains files that will not move - thus freeing the namespace for creating the new directory structure.

4. *Create directory* operations are issued for creating the new directory structure, as described by the list of final paths. This provides final destinations for all the files that are to be moved.

5. *Move file* operations are issued such that all files are moved from the staging directory to their final positions in the base directory (which now contains the new file structure).

6. Finally, *Remove directory* operations are issued, tearing down the staging directory and the structure within.

Note how this plan is relatively inefficient in the number of operations, in that all files will move twice, and destination directories may be torn down and re-created with the same name. Nevertheless, this particular order of operations avoids many corner cases with case sensitivity, permissions, etc. that a more exact implementation would have to tackle. Additionally, should the program fail mid-rename, it is much easier to deduce the stage of the rename (and thus revert it correctly) from any given intermediary position with this algorithm.
