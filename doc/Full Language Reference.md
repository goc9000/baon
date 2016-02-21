BAON
====

(C) Copyright 2012-present Cristian Dinu (<goc9000@gmail.com>); Licensed under the GPLv3.

---

**WORK IN PROGRESS - THIS IS IN THE PROCESS OF BEING REWRITTEN**

---

Full Language Reference
-----------------------

## Pattern Matches

Pattern matches are the most basic building block of any rule. They specify a pattern that the incoming filename text must fit in order for it to be transformed through actions and thus cause the filename to change.

### Elementary Pattern Matches

#### Literal Text Match

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
  - If you need to use the same kind of quote as the one the pattern is delimited by, double it like this: `'Pan''s Labyrinth'`. BAON will interpret this as *<<Pan's Labyrinth>>*.

#### Number Match

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

- `%paras` : Matches text enclosed within parantheses, including the parantheses themselves and any leading whitespace. Thus, this matches `(1984)`, `__(1984)`, `(_radio_mix_)`, `()`, but not:
  - `(1984)__` (trailing whitespace)
  - `abc(def)` (has other text besides the parantheses)
  - `(abc(def))` (nested parantheses are not allowed; such use is not common in filenames anyway)

- `%braces`, `%curlies` : As above, but for straight braces `[` `]` and curly braces `{` `}` respectively.

- `%path` : Matches incoming text in the form of a path leading up to a filename, save for the filename itself. In practical terms this means everything up to the last `/` character, inclusive (or `\` on Windows). If there is no such path separator in the incoming text at all, it is assumed that it consists entirely of a filename, and the match succeeds, but covers an imaginary empty span of text at the beginning of the filename text.

---

REWRITING POINT HERE

---

Many of these may be familiar to C programmers as they closely resemble the format specifiers for `scanf` (but watch out for any differences!).

* `/regular expresssion/` : Matches using the given regular expression (Python flavor) between the delimiters. To include the delimiter character in the regular expression use `//`. You can specify regular expression flags by adding lowercase letters right after the rightmost delimiter. At the moment, the only specifier supported is `i`, for case-insensitive matching.

* `^` : Matches the very beginning of the filename. No text is consumed.

* `$` : Matches the very end of the filename. No text is consumed.

* `%inparas` : Similar to the above, but matches only the enclosed text itself. Mostly useful in search-and-replace matches; for instance, `@%inparas->lower` will make any text enclosed in parantheses lowercase.

* `%braces`, `%inbraces` : As above, but for straight braces, i.e. `[` and `]`.

* `%curlies`, `%incurlies` : As above, but for curly braces, i.e. `{` and `}`.

### Actions

Actions are introduced by the `!`, `->` or `>>` characters right after a match. Actions may be chained, so that the result of one is fed into another, e.g. `%s->action1->action2`. BAON supports the following actions:

* `!` : Deletes the matched text (i.e. transforms it to the empty string). This is useful for removing unwanted junk from a filename.

* `->'exact text'` or `->"exact text"` : Replaces the matched text by the exact text given.

* `->%Nd` : Reformats the matched text as a number with exactly N characters, padded with leading zeroes where necessary. Leading and trailing whitespace is preserved. It is an error if the matched text is not a number.

* `->(rule1; rule2...)` : Passes the matched text through a set of rules. The ruleset between the braces operates within its own separate context; none of its side effects will be visible to matches in the main ruleset.

* `->function` : Applies a built-in function to the matched text. At the moment the following functions are supported:

    * `->trim` : Removes leading and trailing whitespace from the matched text.
    
    * `->upper` : Converts all letters in the matched text to uppercase.
    
    * `->lower` : Converts all letters in the matched text to lowercase.

    * `->title` : Applies title case to the matched text. This mainly involves setting the first letter in every word to uppercase, with some caveats (particle words such as "an", "on", etc., as well as all-uppercase words that probably represent acronyms, are left alone)
    
    * `->unbrace` : Removes all parantheses and braces from the matched text.
    
    * `->paras` : Adds parantheses around the matched text. Note that any leading or trailing whitespace will remain outside the parantheses, e.g. `'  test '->paras` produces `  (test) `.
    
    * `->inparas` : Returns the text between the first pair of matching parantheses in the matched text. Nested parantheses are not supported. An empty string will be returned if there are no matching parantheses in the text.
    
    * `->braces`, `->inbraces` : As above, but for straight braces, i.e. `[` and `]`.
    
    * `->curlies`, ->incurlies` : As above, but for curly braces, i.e. `{` and `}`.

* `>>alias` : Saves the matched text to a location identified by the given alias, while performing no other modification. The text can subsequently be pasted in another place within the filename.

### Insertion Matches

These special match constructs are used to insert text at various places within the filename. They fit within the match framework in that they produce "matched text" that can be subsequently passed to actions. However, the matched text does not correspond to anything in the filename at that position. Insertion matches consume no text and always succeed.

* `<<'exact text'` or `<<"exact text"` : Pastes the exact text supplied.

* `<<alias` : Pastes the text stored under the given alias. This can be used for moving text from one part of the filename to another. It is allowed for the alias capture to occur at a later point in the match sequence, but anything more complicated than that has undefined results.

### Optional and Repeated Matches

The characters `?`, `*` and `+` may be placed after a match to provide effects similar to the ones they have in regular expressions:

* `?` makes the previous match optional. This means that, if the match fails, instead of the entire containing sequence failing, the matched text for this component will be empty and no text will be consumed.

  Note that any side-effects within the match (i.e. saving aliases, partial text consumption if the match is a complex sequence, etc.) will be undone if the match fails.

* `*` repeats the match until failure. The matched text will consist of the concatentation of the matched texts for every instance of the match. If the match never succeeded once, the matched text will be empty as for the `?` case.

  Be sure to understand how repeat operators combine with actions:
  
  * `match1*->action1` means : apply *match1* repeatedly, concatenate the results, and apply *action1* to the final result.

  * `match1->action1*` means : apply *match1* repeately, apply *action1* individually to the matched text for each instance, then concatenate the individual results and return that as the final output.

  * `match1->action1*->action2` : as above, then apply *action2* to the combined results.
 
* `+` works like `*`, but requires that the match succeed at least once. If it does not, the normal semantics for a failed match apply.

### Match Sequences

The most common way of combining matches is to place them in a *sequence*. This is achieved by simple juxtaposition:

    match1  match2  match3  etc.

The matches contained in a sequence will be executed in order. Each match will try to match text starting at the point where the previous one ended. Additional context effects such as alias setting will also be inherited.

If, and only if, all of the component matches succeed, the result of the match sequence will be the concatenation of the individual match results. Otherwise, if any of the components fails to match, the match sequence itself will fail and any effects such as text consumption will be undone.

One can note that this description is very similar to that of a rule. In fact, most rules consist of a single match sequence, but more complex constructions are possible, as we will see below.

### Special Match Constructs

#### Subrules

Groups of matches can be enclosed in parantheses so as to form a 'subrule' that is treated as a single match. For instance, we can have a sequence like:

    match1  (match2  match3)->action23?  match4  etc.

After `match1` succeeds, a match of the sequence `match2 match3` will be attempted. If the group succeeds, its matched text will be transformed according to `action23` and matching will continue with `match4`. Otherwise, the failed match semantics will apply for the entire group; due to the presence of the `?` operator, the context will be reset to the point after `match1` succeeded, and execution will continue with `match4`.

#### 'Between' Matches

'Between' matches are represented by the symbol `..` and are generally placed in sequences, like:

    match1  ..  match2

Intuitively speaking, a `..` specifier will match all of the text *between* the matches that enclose it. For instance, the sequence:

    %d  '. '  ..->title  '('
    
means that we will first consume a number, then the sequence `'. '`, and then we will look for a paranthesis up ahead. When we have found one, all of the text from the end of the `'. '` sequence up to the open brace will be passed through the `title` filter. Therefore, between matches are a convenient way to avoid specifying a complex pattern for content that is best described by its position between two simpler patterns.

Caveats:

* A `..` with no preceding match will simply match text from the beginning of the incoming text to the first occurence of the following match.

* A `..` placed at the very end of a sequence will match everything up to the end of the incoming text. This may not be what you expected, especially this occurs at the end of a subrule. For instance, in the sequence `m1 (m2 ..) m3`, if both `m1` and `m2` succeed, the `..` will match all of the remaining text in the rule, and only then will a match of `m3` be attempted on the (empty) remaining text. The `..` specifier does not 'see' any subsequent matches if they occur at a higher level.

* In parser parlance, the `..` match is not greedy and does not backtrack. This means that in an example such as:

  `01. Diamond Dogs - David Bowie - 1974.mp3`
  
  with the rule `%d  ..  ' - '  %d`, the match will always fail because the first `' - '` found will always be picked, even though picking the second one is the only way for the global match to succeed.

#### Search-and-Replace Matches

Search-and-replace matches are introduced by specifying the `@` character before a match. This radically alters the semantics of the succeeding match in the following way: the match will be looked for repeatedly anywhere in the incoming text, and wherever it succeeds, the matched portion of the incoming text will be replaced by the match result. The transformed incoming text will then be visible to all following matches. For instance:

    match1  @' '->'/'  match2
  
will mean that all incoming text remaining after `match1` will be transfomrmed so as to replace all spaces with slashes. The `match2` specifier and all subsequent ones will operate on this modified version of the incoming text.

Note that, like all context effects, modifications to the incoming text persist even across parantheses. For instance, in the sequence:

    m1  (m2  @m3->a3  m4)?  m5

matches `m1` and `m2` will operate on the original incoming text; both matches `m4` and `m5` will see the incoming text as modified by `m3`; however, if the `m2`..`m4` subrule fails, the modifications will be cancelled, so that `m5` will also operate on the original text.

#### Alternatives ('OR' Matches)

The final special match in our toolset is the 'or' match. This is introduced by using the `|` operator in between matches that represent alternative ways of representing a filename. For instance, in the rule:

    match1  match2  |  match3  |  match4  match5  match6

The text will first be matched against the sequence `match1  match2`, then, if this fails, against `match3`, then, if this fails as well, against `match4  match5  match6`. The first alternative that succeeds will represent the result of the entire rule. If all alternatives fail the rule fails as well.

If you want to use the `|` operator for alternative ways of matching a single filename component, you will have to use braces, e.g.:

    match1  (match2  |  match3)  match4

matches `match1`, then either `match2` or `match3`, whichever suceeds first, then finally `match4`.
