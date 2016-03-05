BAON
====

(C) Copyright 2012-present Cristian Dinu (<goc9000@gmail.com>); Licensed under the GPLv3.

---

**WORK IN PROGRESS - THIS IS IN THE PROCESS OF BEING REWRITTEN**

---

Full Language Reference and Tutorial
====================================


Table of Contents
-----------------

1. [Pattern Matches] (#pattern-matches)
  1. [The Literal Text Match] (#the-literal-text-match)
  2. [The Number Match] (#the-number-match)
  3. [Advanced Pattern Matches] (#advanced-pattern-matches)
  4. [The Regular Expression Match] (#the-regular-expression-match)
2. [Actions] (#actions)
  1. [Basic Text Processing Actions] (#basic-text-processing-actions)
  2. [Capitalization Actions] (#capitalization-actions)
  3. [Brace Processing Actions] (#brace-processing-actions)
  4. [Number Processing Actions] (#number-processing-actions)
  5. [The Save to Alias Action] (#the-save-to-alias-action)
  6. [The Apply Subrules Action] (#the-apply-subrules-action)
  7. [Chaining Actions] (#chaining-actions)
3. [Combining Matches] (#combining-matches)
  1. [Matches in a Sequence] (#matches-in-a-sequence)
  2. [Grouping Matches with Parantheses] (#grouping-matches-with-parantheses)
  3. [Match Alternatives] (#match-alternatives)
  4. [Optional Matches] (#optional-matches)
  5. [Repeated Matches] (#repeated-matches)
4. [Insertions] (#insertions)
  1. [The Literal Text Insertion] (#the-literal-text-insertion)
  2. [The Alias Insertion] (#the-alias-insertion)
5. [The 'Between' Match] (#the-between-match)


Pattern Matches
---------------

Pattern matches are the most basic building block of any rule. They specify a pattern that the incoming filename text must fit in order for it to be transformed through actions and thus cause the filename to change.

### Elementary Pattern Matches

#### The Literal Text Match

The simplest possible pattern match is the **literal text match**, which is specified like this:

    'Exact text'

Or

    "Exact text"

The incoming text is considered to fit the match if it **exactly** equals the text between the quotes. We then say that the match *succeeds*, and the text will be transformed according to any actions specified after the match.

Notes:
- By "exactly equals" we mean that all letters and spaces are in the same place, same amounts and same case ('A' is not equal to 'a'). Thus, the pattern `"abc DEF"` matches the text `abc DEF` but not:
  - `Abc Def` (different case)
  - `abc__DEF` (has extra whitespace; `_` has been used to represent space for clarity)
  - `_abc_DEF` (has leading whitespace)
  - `abc_DEF_` (has trailing whitespace)
  - `ăbc DEF` (accented characters are not the same as the base character)
- The pattern can include Unicode characters like national characters (e.g. `Ă`, `ș`, `ț`), symbols like the em dash, etc. Just type them in directly as you would any other letter.
- There is no mechanism for specifying special characters by their ASCII code or Unicode code point. Even assuming the operating system lets you, putting characters in filenames that cannot be easily typed is nearly always a bad idea.
- Some operating systems allow the quotes or double-quotes themselves to be part of a filename. To make a quote or double-quote part of the pattern, you have two options:
  - Type it directly, while making sure the pattern is delimited by a quote of a different kind, so that there is no confusion. For instance, `"Pan's Labyrinth"` (single quote inside double quotes) or `'Louis "Pops" Armstrong'` (double quotes inside single quotes)
  - If you need to use the same kind of quote as the one the pattern is delimited by, double it like this: `'Pan''s Labyrinth'`. BAON will collapse the repeated single quote and interpret the text as `Pan's Labyrinth`.

#### The Number Match

Another very commonly used pattern is the **number match**, which takes the form:

    %d

It matches incoming text in the form of a **positive integer**, *including any leading zeroes and leading whitespace*.

Thus, `%d` matches:

- `1`
- `1234`
- `003`
- `__004`

But not:

- `123__` (trailing whitespace)
- `-45` (has sign)
- `12.4` (is not an integer)
- `12a` (has other characters)

The reason for these particular limitations is that this pattern is intended for use with track numbers and years, which are the most common uses of numbers in filenames.

A variant of this match is the **fixed width number match**, which is specified like this:

    %5d

Or `%1d`, `%2d`, `%15d` etc. This matches a **number consisting of exactly N digits** (where *N* is the number between the `%` and `d`), including any leading whitespace. Thus, `%5d` matches:

- `12345`
- `00123`
- `___12345`

But not:

- `12345__` (trailing whitespace)
- `123` (shorter)
- `123456` (longer)
- `0012345` (leading zeroes are part of the count, so still too long)

### Advanced Pattern Matches

For more exotic use cases, these patterns are available:

- `%s` : Matches a **word**, including any leading whitespace. A word is defined as any sequence of contiguous characters (including digits and punctuation), up to the first whitespace character. Thus, this matches `abc`, `__abc`, `abc-def`, `abc5.3`, but not `ab_cde` (a word only lasts until a space, so this is actually two words).

- `%Ns` : Matches a word consisting of exactly *N* characters, including any leading whitespace. The leading whitespace does not count towards the limit. Thus, `%4s` matches `abcd`, `__abcd`, `a-b5` but not `abc`, `_abc`, `abcde` etc.
 
- `%c` : Matches a single character, including whitespace. Thus, `%c` matches `a`, `b`, `5`, `!`, `_`, etc. Note that since any character is accepted, the only way this can fail to match is if the incoming text is empty, e.g. when all of the filename has already been covered by previously encountered matches and we are at the very end of it.

- `%Nc` : Matches a sequence of exactly *N* characters, including whitespace characters which are also part of the count. Thus, `%4c` matches `abcd`, `ab12`, `ab_c`, `___a`, `____` etc. As for `%c`, since any character matches, this will always succeed unless there are fewer than *N* characters left in the incoming text.

- `%ws` : Matches any amount of whitespace (including none at all).

- `%parens` : Matches text enclosed within parentheses, including the parentheses themselves and any leading whitespace. Thus, this matches `(1984)`, `__(1984)`, `(_radio_mix_)`, `()`, but not:
  - `(1984)__` (trailing whitespace)
  - `abc(def)` (has other text besides the parentheses)
  - `(abc(def))` (nested parentheses are not allowed; such use is not common in filenames anyway)

- `%braces`, `%curlies` : As above, but for straight braces `[` `]` and curly braces `{` `}` respectively.

- `%path` : Matches incoming text in the form of a path leading up to a filename, save for the filename itself. In practical terms this means everything up to the last `/` character, inclusive (or `\` on Windows). If there is no such path separator in the incoming text at all, it is assumed that it consists entirely of a filename, and the match succeeds, but covers an imaginary empty span of text at the beginning of the filename text.

### The Regular Expression Match

For when you need maximum control over the pattern that the incoming text should fit, BAON supports **regular expression matches**, specified like this:

    /pattern/

i.e. the [regular expression](https://en.wikipedia.org/wiki/Regular_expression) should be delimited by `//`. For instance:

- `/\s*[0-9]+/` will match a positive integer optionaly preceded by whitespace or leading zeroes, and thus exactly duplicate the functionality of `%d`.
- `/([A-Za-z]+-)*[A-Za-z]/` will match a single word (e.g. `Dylan`) or hyphenated combination of words (e.g. `Jay-Z`), useful for names.

Notes:
- Practical regular expressions used in various environments and programming languages exhibit particular variations from the theoretical standard, called *flavors*. BAON is written in Python and thus uses [Python flavored regular expressions](https://docs.python.org/3.4/howto/regex.html).
- By default, the regular expression is case sensitive, i.e. case differences matter. For instance, `/[a-z]+/` matches a sequence of lowercase letters only. To ignore case differences, append `i` after the last delimiter, e.g. `/[a-z]+/i` matches a sequence of both lowercase and uppercase letters.


Actions
-------

Before going into yet more advanced match types, it is necessary to introduce the second fundamental concept of **actions**. Actions specify what is to be done with the incoming text that fits the pattern described by matches, and thus how BAON fulfills its primary function of changing filenames such that files are renamed of moved.

Actions are introduced by the `!`, `->` or `>>` characters right after a match. For instance:

    'Album'->upper

Has the following effect: if the incoming text matches the pattern described by `'Album'` (i.e. consists of that word in that exact spelling), that part of the text will be converted to uppercase (this is what the `->upper` action means), and thus the file will be renamed accordingly. Otherwise, if there is no match, the action will not be performed and the filename will remain unchanged. Thus, a directory named `Album` will be renamed to `ALBUM`. A file or directory with any other name, say, `Booklet`, or `01. Overture` will be left alone.

BAON supports a limited number of powerful actions, divided into several categories:

### Basic Text Processing Actions

- `!` : Deletes the matched text. This is useful for removing unwanted junk from a filename. E.g. `'The '!` will delete the `The` particle from the beginning of a filename, if it starts with that particle.

- `->'exact text'` or `->"exact text"` : Replaces the matched text by the exact text between the quotes (syntax is the same as for the literal text match). E.g. `'Ouverture'->'Overture'` will translate between the French and the English spelling of that musical term.

- `->trim` : Removes leading and trailing whitespace from the matched text. Thus, `_ab_c__` becomes `ab_c`.

### Capitalization Actions

- `->upper` : Converts all letters in the matched text to uppercase. E.g. `AbcDE` becomes `ABCDE`.
    
- `->lower` : Converts all letters in the matched text to lowercase. E.g. `AbcDE` becomes `abcde`.

- `->title` : One of the most common and powerful actions, this changes the capitalization of the matched text so as to conform to the English rules for titles. Thus, most words will have their first letter converted to uppercase and the rest to lowercase, with some exceptions made for special situations (e.g. particles like *on*, *and*, *the*, acronyms, etc.). For instance, the text `the girl In tHE paRK` becomes `The Girl in the Park`.

### Brace Processing Actions

- `->unbrace` : Removes all parentheses and braces from the matched text. E.g. `(remix[4])` becomes `remix4`.
    
- `->parens` : Adds parentheses around the matched text. Note that any leading or trailing whitespace will remain outside the parentheses, e.g. `'__test_'->parens` produces `__(test)_`.
    
- `->inparens` : Keeps only the text between the first pair of matching parentheses in the matched text. Nested parentheses are not supported. If there are no matching parentheses in the text, it will be completely deleted. E.g. `'Track 01 (radio mix)'->inparens` produces `radio mix`.
    
- `->braces`, `->inbraces` : As above, but for straight braces, i.e. `[` and `]`.
    
- `->curlies`, `->incurlies` : As above, but for curly braces, i.e. `{` and `}`.

### Number Processing Actions

- `->%Nd` : Reformats the matched text as a number with exactly *N* characters, padded with leading zeroes where necessary. Leading and trailing whitespace is preserved. It is an error if the matched text is not a number. Thus, if the action is `->%3d`:
  - `24` becomes `024`
  - `01` becomes `001`
  - `123` remains `123`
  - `1234` remains `1234`
  - `___12_` becomes `___012_`
  - `abc` causes an error and the file will not be renamed

### The Save to Alias Action

- `>>alias` : Saves the matched text to a variable (called an **alias**) whose name is given after the `>>`. For instance, `%d>>year` will look for a number in the incoming text, and save it in a variable called *year*. This text can be re-inserted into another part of the filename using the **insertion** constructs described in a later section.

### The Apply Subrules Action

- `->(rule1; rule2...)` : Passes the matched text through a set of rules, as if it was a filename in itself. For instance, if we have:

  `%s->(%d->%3d; '000'->'Cover')`
  
  The effects will be as follows:
  - Given the first word in the incoming text (`%s`):
    - Apply subrule 1 (`%d->%3d`) : if the word starts with a number, that number will be reformatted so as to have 3 digits (including leading zeroes)
    - Then apply subrule 2: (`'000'->'Cover'`) : if the transformed word resulting from applying the previous rule begins with `000`, that part will be replaced with the word `Cover`.
  - The word has now been transformed according to the two rules.

  Note: the rules within the parentheses can use aliases saved in the main rules, and viceversa.

### Chaining Actions

The final lesson in using actions is that they can be *chained* such that multiple actions apply to the result of a successful match, without needing to use the 'apply subrules' action. The result of one action will feed into another. For instance:

    %d->%4d>>year!
  
Will have the following effect:

  - If the incoming text matches a number (`%d`):
    - Extend it to 4 characters (`->%4d`)
    - Save the extended number to the alias *year* (`>>year`)
    - And finally, delete the number from the place we found it (`!`)

Note that the deletion of the number does not affect the value stored in the alias (as long as the deletion is specified *after* the save). In fact, storing the result of a match to an alias and then deleting it, then using the alias in an insertion later, is a common way of reordering parts of a filename (e.g. moving the artist name from the beginning to the end of a filename or viceversa).


Combining Matches
-----------------

In order to achieve complex matching and transformation, BAON provides a series of ways to combine and group the elementary matches described above.

### Matches in a Sequence

The simplest way of combining matches is to place them in a **sequence**, by simply putting them one after the other, separated by whitespace:

    match1->action1 match2->action2 match3->action3 ...

Matches in a sequence will be processed in order:

  - First, the incoming text will be matched against the pattern for *match1*. If it fits, the portion of the text that matched will be transformed according to *->action1*. The matched text will then be considered *consumed*, such that subsequent matches will look at the incoming text just past the part that matched.
  - Then, the *remaining* incoming text will be matched against the pattern for *match2* and transformed according to *->action2*. The part of the text that matched will be consumed.
  - Then, the *remaining* incoming text will be matched agains *match3* etc.
  - **If, and only if, all the matches were successful**, the resulting incoming text will consist of the transformed matched text for *match1*, followed by the transformed text for *match2*, etc.
    - If there are any matches after the sequence (which is possible using some of the operators described in future sections), they will act on the text that remains after all of the matches in the sequence have consumed their correspoding bits of matched text.
  - Conversely, **if any of the matches fails** (the text at that point does not fit the pattern), **the entire sequence match will fail** and any modifications made by *match1*, *match2*, etc. up to the failed match will be **cancelled**.

To illustrate with a concrete example:

    %d->%02d ' - '->'. ' %s %parens!

- `%d->%02d` : First, we will expect a number (e.g. a track number), and reformat it so that it has 2 digits.
- `' - '->'. '` : Then, we will expect a space-flanked dash that separates the track number from the rest of the filename. We will change this into a period, a different style of punctuating the track number.
- `%s`: Then, we will expect a single word. This will not be transformed in any way, it just needs to be there.
- `%parens`: Finally, we will expect some parenthesized text to follow (like `(remix)`) and delete it.

A filename that can match this sequence is `1 - Overture (original cut)`. It will be processed as follows:

| Match+Action  | Matched Text      | Transformed Text |
|---------------|-------------------|------------------|
| `%d->%02d`    | `1`               | `01`             |
| `' - '->'. '` | `_-_`             | `._`             |
| `%s`          | `Overture`        | `Overture`       |
| `%parens`     | `_(original_cut)` | *(empty text)*   |

for a full result of `01. Overture`

The following filenames will **not** match the sequence and will thus be left unmodified:

- `Cover Art` (does not start with a number, `%d` fails)
- `01. Overture (original cut)` (the track number is not separated by a dash, `' - '` fails)
- `01 - Overture` (there is no text in parentheses, `%parens` fails)
- `01 - Allegro assai (overture)` (the `%s` matches against the word `Allegro`, then the `%parens` fails because the word `assai`, still unconsumed, lies before the parenthesized text that would otherwise match)

### Grouping Matches with Parantheses

You can put parentheses around several matches in a sequence to mark them as part of a **group**. This does not affect their functioning, but allows you to treat them as a single match in certain operations. In particular, it allows you to add actions that act on the entire group. Actions on a group will take effect on the complete text covered by all the matches, after it has been transformed by the actions on the individual matches contained within the group. For instance:

    %d (%d->parens %d->parens)->braces %d

applied to `1 2 3 4` will yield:

    1 [(2) (3)] 4

The two `%d`'s in the group each matched the text `_2` and `_3` respectively, and then transformed it to `_(2)` and `_(3)` respectively according to their actions. Finally, the `->braces` action was applied to this group, and it transformed the complete text, `_(2)_(3)` to `_[(2)_(3)]`.

Groups can be nested, as in this example:

    %d (%d (%d %d)->braces %d)->parens %d

It is also possible to form a group with just one match (though generally useless).

### Match Alternatives

By using the `|` character to separate matches within a rule or paranthesized group, you can set up **match alternatives**. This means that in this example:

    match1 (match2 match3 | match4) match5

BAON will first try to fit the incoming text according to the pattern described by `match1 match2 match3 match5` (i.e. it considers the first alternative). If this fails, it will then backtrack and switch to the second alternative, and attempt to fit the text to `match1 match4 match5`. If this also fails, the alternatives will have been exhausted and the filename will be left unmodified.

For a more concrete example:

    %d->%2d (' - '->'. ' | '. ') %s->upper

Will handle both:

    1 - overture

and

    1. overture

transforming them both to `01. OVERTURE`.

In the first case, first the track number will be matched and transformed, and then BAON will go with the first alternative, find the `_-_` and transform it to `._`. Finally, the track title will be found and transformed to uppercase. In the second case, the track number will be transformed, and then BAON will go with the first alternative, see that it doesn't match, then try the second. `._` does match, and thus we continue again to the `%s` matching the track title, which is then uppercased. Conversely, a filename like `1--overture` would be left unchanged because it matches none of the alternatives.

Notes:

- You can specify more than two alternatives, and any number of alternative groups within a rule:

  `match1 (match2 match3 | match4 | match5 match6) (match7 | match8)`

  This will attempt to match the incoming text against the following 6 patterns, in order:
  - `match1 match2 match3 match7`
  - `match1 match2 match3 match8`
  - `match1 match4 match7`
  - `match1 match4 match8`
  - `match1 match5 match6 match7`
  - `match1 match5 match6 match8`

- If the `|` is not used within a paranthesized group, the scope of the alternative will be the entire rule text. Thus, in this example:

  `match1 match2 | match3`
  
  The two alternatives are `match1 match2` and `match3`, not `match1 match2` and `match1 match3`.

- Actions can be attached as normal to a paranthesized group that contains alternatives. The text they act on will be the matched and transformed text for the alternative that was selected in the end by BAON.

### Optional Matches

Adding the character `?` after a match makes it **optional**. This indicates to BAON that the match can be skipped if it either fails, or if it should be skipped in order for the rest of the matches to succeed.

For instance:

    %s %d? %s

will match both of:

  - `Time 2 Die` (all three matches succeed)
  - `Time Die` (the `%d` match fails but is skipped)

Somewhat less obviously, it will also match:

    `Time 2`

What happens here is that the `%d` match does succeed, but this leaves no text for the final `%s` to match. Thus BAON backtracks and skips the match, allowing the final `%s` to match with the `_2`. In retrospect, this makes sense, since the text would be matched by the pattern `%s %s` where we omitted the optional match outright.

Essentially, the behavior of `?` can best be understood by the metaphor that BAON will first see the match as mandatory and try to fit the pattern; if it fails, it will remove the match and try to fit again; if this fails as well, it will finally give up. Another way of expressing this is to consider that:

    match?

is equivalent to:

    (match | '')

Notes:

- The operator applies to normal matches and anything that behaves as a single match, in particular paranthesized groups. Thus one can often find constructs like:

  `match1 (match2 match3)? match4`

- The original match in combination with the `?` sign are seen as a single match (without needing to use parantheses), to which actions can also be attached, as in this example:

  `match->action1->action2?->action3->action4`
  
  Here, `match->action1->action2` is the original match with two actions attached. To this we add the `?` sign to make it optional, and to this combined match we also add two more actions, `->action3->action4`. Note that unlike the actions attached to the original match, these will *always* be executed regardless of whether the match was skipped or not. If the match succeeded, they will apply to the matched text and basically chain with `->action1->action2`. If the match was skipped, they will apply to the empty text, as if the match had been just `''`. For instance:
  
  `%s %d->parens?->braces %s`
  
  - applied to `Time 2 Die` will produce `Time [(2)] Die`
  - applied to `Time Die` will produce `Time[] Die`
  
  Note that the 'put in parantheses' action was only performed when we actually found a number. However, the 'put in braces' action was performed in both cases, first on the already-parenthesized number, and, when no number was found, simply on the empty text.

- Any number of optional matches can be present in a rule, and their backtracking behavior is the same as for the alternatives match.

### Repeated Matches

Adding the `+` character after a match will change its operation so that it is **repeated** until the incoming text no longer fits the pattern, after which processing will continue with the next match. For instance, whereas `%d 'Go'` matches:

- `1 Go` (a single word followed by 'Go')

But not:

- `1 2 3 Go`

By applying `+` to `%d` we get `%d+ 'Go'` which can match:

- `1 Go`
- `1 2 3 Go`,
- `6 0 3 1 Go`, and in general any amount of numbers followed by a 'Go'.

Notes:

- The pattern has to fit at least once for the match to be successful. If it doesn't fit even once, the usual semantics of a failed match apply (i.e. the containing sequence also fails etc.). There is an alternative operator, `*`, which works the same except zero repetitions are allowed. In fact, you can think of `*` as a cross between `+` and `?`.
  - As a technical note, the symbols for `?`, `+` and `*` were not chosen arbitrarily, they are very similar in form and function to the same operators as found in [regular expressions](https://en.wikipedia.org/wiki/Regular_expression).

- As for the optional match, the match and `+` together also form a single match-like entity to which actions can be applied. The significance of the actions is as follows:
  - The actions on the original match apply to the matched text on every repetition
  - The actions on the overall match apply to the entire text that was covered by all the repetitions, after it has been transformed by the attached actions.
  
  For example, if we apply the match `%d->parens+->braces 'Go'` to the text `1 2 3 Go`, the result will be:

  `[(1) (2) (3)] Go`
  
  i.e. the `->parens` action was applied on every repetition, as if the match had been `%d->parens %d->parens %d->parens`, whereas the `->braces` action was applied on the entire matched and transformed text `_(1)_(2)_(3)`.

- BAON will *backtrack* on repeat matches just like it does on optional matches. This means that, initially, BAON will repeat the match as many times as possible (until the text no longer fits). If there is a failure in the matches after the repeated match, instead of giving up, BAON will return to the repeated match and do one less repetition, in the hopes that this will allow the remaining text (which now also includes the part that would have been consumed by the last repetition) to fit the pattern of the remaining matches. This continues with fewer and fewer repetitions, until either the overall match succeeds, or we go down to 0 repetitions, in which case BAON finally gives up.

  This behavior is what allows a pattern like `%d+ %d 'Go'` to also fit `1 2 3 Go`. BAON will go through the following steps:
  
  - First, it will allow the first `%d+` to go as far as possible. It will match and consume the initial `1 2 3`.
  - BAON now has to match the second `%d` against the remaining `Go`, which fails
  - It then backtracks to the first `%d+` and does one less repetition so that it only consumes `1 2`
  - Then, the second `%d` successfully matches against the `3`
  - Finally, the `'Go'` matches with the remaining `Go` and the overall process succeeds.


Insertions
----------

Whereas *matches* fit text and transform it, **insertions** are constructs that add text regardless of what is already in the filename. BAON supports two types of insertions:

### The Literal Text Insertion

Literal text insertions are specified like this:

    <<'exact text'

or:

    <<"exact text"

The effect is the insertion of the specified text at the current position, without any incoming text being consumed. For instance, given a track filename like:

    01. sorry seems to be the hardest word

The rule:

    %d '. ' <<'ELTON JOHN - ' %s+->title

Will transform it to:

    01. ELTON JOHN - Sorry Seems to Be the Hardest Word

Note how the insertion added the artist name prior to the rest of the title words being captured by another match and recapitalized.

Notes:

- The quoting rules are the same as for the literal text match or the 'replace by literal text' action.
- Other than not actually matching any text, insertions behave like matches in that they can be grouped and support actions. Actions are generally not useful with literal text insertions, but rather with the *alias insertions* described in a future section. 
- In fact, an insertion is almost equivalent to a match like:

  `''->'exact text'`
  
  except it behaves differently when placed after expanding constructs like a match with `+` or `*`, or `..`. Essentially the insertion does not limit the expansion of these constructs as a match would. Instead, they will be expanded up to the first "real" match that follows.

### The Alias Insertion

**Alias insertions** are specified like this:

    <<alias

The effect is the insertion of the text that was stored in the *alias* with that name, by a corresponding *store to alias* action.

Alias insertions and store-to-alias actions work together to allow parts of the filename to be moved around or duplicated. For instance, this will move the track number from the beginning to the end of a filename:

    %d>>trackno! '. '! %s+ <<' (track ' <<trackno <<')'

Thus turning:

    01. Overture

into:

    Overture (track 01)

Note how `>>trackno` is used to store the track number to the *trackno* alias, which is then deleted via `!` from its initial place at the start of the filename. Later on, the track number is re-inserted into the proper place via the `<<trackno` insertion.

Notes:

- It is possible to refer to an alias that is stored at a later point in the match. This happens often when moving things from the end to the beginning of the filename. For instance, a rule to undo the previous example would look like:

  `<<trackno <<'. ' %s+ '(track '! %d>>trackno ')'!`

  In such situations, BAON will try to do the smart thing and constructs like this will work as expected, and even more complicated ones in which text inserted by aliases is itself put into other aliases, etc.

- If you refer to an alias that is not stored to, even later in the match, the insertion will have no effect (the alias will be seen as containing empty text).

- Actions can be applied to alias insertions, causing the text to be transformed as it is inserted. For instance, a track number with no leading zeroes could have them inserted like this:

  `>>trackno! %s+ <<' (track ' <<trackno->%2d <<')'`


The 'Between' Match
-------------------

The **'between' match** is a very useful and common construct, represented by the symbol `..`. It is generally placed in sequences, like:

    match1  ..  match2

Intuitively speaking, a `..` match will fit all of the text *between* the matches that enclose it. For instance, the sequence:

    %d  '. '  ..->title  '('
    
means that BAON will first consume a number, then the `'._'` separator, and then it will look for a parenthesis up ahead. When it has found one, all of the text from the end of the `'._'` up to the open brace will be passed through the `title` filter. Therefore, between matches are a convenient way to avoid specifying a complex pattern for content that is best described by its position between two simpler patterns.

Notes:
- A `..` can also be used with no preceding or following match, in which case it will fit text from the very beginning of the filename or to its end, respectively.
- A `..` right after another `..` will never be expanded. Any actions on it will act only on empty text.

---

REWRITING POINT HERE

---

## Search-and-replace

## Positional matches

- mention regexes again, note that their positional features can be used


* `^` : Matches the very beginning of the filename. No text is consumed.

* `$` : Matches the very end of the filename. No text is consumed.

* `%inparens` : Similar to the above, but matches only the enclosed text itself. Mostly useful in search-and-replace matches; for instance, `@%inparens->lower` will make any text enclosed in parentheses lowercase.

* `%braces`, `%inbraces` : As above, but for straight braces, i.e. `[` and `]`.

* `%curlies`, `%incurlies` : As above, but for curly braces, i.e. `{` and `}`.



## rules and rulesets




#### Search-and-Replace Matches

Search-and-replace matches are introduced by specifying the `@` character before a match. This radically alters the semantics of the succeeding match in the following way: the match will be looked for repeatedly anywhere in the incoming text, and wherever it succeeds, the matched portion of the incoming text will be replaced by the match result. The transformed incoming text will then be visible to all following matches. For instance:

    match1  @' '->'/'  match2
  
will mean that all incoming text remaining after `match1` will be transfomrmed so as to replace all spaces with slashes. The `match2` specifier and all subsequent ones will operate on this modified version of the incoming text.

Note that, like all context effects, modifications to the incoming text persist even across parentheses. For instance, in the sequence:

    m1  (m2  @m3->a3  m4)?  m5

matches `m1` and `m2` will operate on the original incoming text; both matches `m4` and `m5` will see the incoming text as modified by `m3`; however, if the `m2`..`m4` subrule fails, the modifications will be cancelled, so that `m5` will also operate on the original text.
