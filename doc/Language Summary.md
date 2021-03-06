BAON
====

(C) Copyright 2012-present Cristian Dinu (<goc9000@gmail.com>); Licensed under the GPLv3.


Language Summary
================


Pattern Matches
---------------

| Form                   | Description                               | Example Usage   | Matching Text Examples       | Non-matching Text Examples          |
|------------------------|-------------------------------------------|-----------------|------------------------------|-------------------------------------|
| `'text'` or `"text"`   | Matches that exact text                   | `'abc'`         | `abc`                        | `AbC` `def` `ab`                    |
| `%d`                   | Matches a number                          | `%d`            | `123` `0012`                 | `notanumber` `-4`                   |
| `%Nd`                  | Matches a number with N digits            | `%4d`           | `4567` `0123`                | `123` `123456` `notanumber`         |
| `%s`                   | Matches a single word or compound word    | `%s`            | `the` `quick` `12`  `pop-up` | `abc def`                           |
| `%Ns`                  | Matches a single word of N letters        | `%3s`           | `the` `123` `abc`            | `abcd` `12` `a b`                   |
| `%c`                   | Matches any single character              | `%c`            | `a` `b` `1` `2` `_`          | N/A (only end of filename)          |
| `%Nc`                  | Matches next N characters                 | `%4c`           | `abcd` `1234` `ab c`         | `a` `12`                            |
| `%ws`                  | Matches any amount of whitespace          | `%ws`           | `_` `___` (empty text)       | `abc`                               |
| `%parens`              | Matches parentheses and the text within   | `%parens`       | `(1984)` `(remix)`           | `abc` `[1984]` `(())` `extra(text)` |
| `%braces`, `%curlies`  | Same, for `[]` and `{}`                   |                 |                              |                                     |
| `%path`                | Matches a path up to a basename           | `%path`         | `abc\def\gh` `abc/d e/f`     | `123`                               |
| `/regular-expression/` | Matches according to a regular expression | `/[a-z]+[0-9]/` | `abc3` `e5`                  | `abc` `3`                           |


Actions
-------

| Form                       | Description                           | Example Usage         | Example Input(s)          | Example Output(s)                 |
|----------------------------|---------------------------------------|-----------------------|---------------------------|-----------------------------------|
| `!`                        | Delete text                           | `!`                   | `abc`                     | (empty text)                      |
| `->'text'` or `->"text"`   | Replace by that exact text            | `->"abc"`             | `x`                       | `abc`                             |
| `->trim`                   | Remove whitespace at start and end    | `->trim`              | `__ab_c_`                 | `ab_c`                            |
| `->upper`                  | Convert to uppercase letters          | `->upper`             | `abc` `Abc123`            | `ABC` `ABC123`                    |
| `->lower`                  | Convert to lowercase letters          | `->lower`             | `ABC` `Abc123`            | `abc` `abc123`                    |
| `->title`                  | Apply capitalization rules for titles | `->title`             | `we'll always have VALIS` | `We'll Always Have VALIS`         |
| `->unbrace`                | Remove all parentheses and braces     | `->unbrace`           | `_(remix[4])`             | `_remix4`                         |
| `->parens`                 | Add parentheses around text           | `->parens`            | `1984` `__remix_`         | `(1984)` `__(remix)_`             |
| `->inparens`               | Extract text from parentheses         | `->inparens`          | `__(remix)_` `noparens`   | `remix` (empty text)              |
| `->braces`, `->inbraces`   | Same, for `[]`                        |                       |                           |                                   |
| `->curlies`, `->incurlies` | Same, for `{}`                        |                       |                           |                                   |
| `->%Nd`                    | Reformat number to have N digits      | `->%3d`               | `0` `12` `1234`           | `000` `012` `1234`                |
| `>>alias`                  | Save text to alias                    | `>>trackno`           | `some text`               | (stores `some text` to `trackno`) |
| `->(rule1; rule2)`         | Transform text according to rules     | `->('abc'!; %d->%2d)` | `abc3` `def`              | `03` `def`                        |
| `->action1->action2`       | Chain actions                         | `->lower->parens`     | `REMIX`                   | `(remix)`                         |


Insertions
----------

| Form                     | Description                 | Example Usage | Example Output                    |
|--------------------------|-----------------------------|---------------|-----------------------------------|
| `<<'text'` or `<<"text"` | Insert that exact text      | `<<"abc"`     | `abc`                             |
| `<<alias`                | Insert text stored in alias | `<<trackno`   | `02` (if `trackno` contains `02`) |


Combining Matches
-----------------

| Form                         | Description                                         | Example Usage           | Matching Text Examples          | Non-matching Text Examples |
|------------------------------|-----------------------------------------------------|-------------------------|---------------------------------|----------------------------|
| `match1 match2 match3 ...`   | Matches `match1` followed by `match2` etc.          | `%d " - " %s`           | `1 - Overture` `004 - abc`      | `abc` `01 - `              |
| `(match1 match2 match3 ...)` | Group matches so that they behave as a single match | `%d (%d %d)->parens %d` | `1 2 3 4` (output: `1 (2 3) 4`) |                            |
| `match1 | match2 | ...`      | Matches `match1` or `match2` etc.                   | `(%d | "abc") %d`       | `1 2` `abc 5`                   | `def 5`                    |
| `match?`                     | Optional match, can be skipped                      | `"Ready" %d? "Go"`      | `Ready 2 Go` `Ready Go`         | `Ready 2`                  |
| `match+`                     | Matches `match` repeated as many times as possible  | `%d+ "Go"`              | `1 Go` `60 31 79 1 Go`          | `Go` `1 2 abc 3 Go`        |
| `match*`                     | Ditto, and also optional                            | `%d* "Go"`              | `Go` `1 2 3 Go`                 | `1 2 3`                    |


Special Matches
---------------

| Form             | Description                            | Example Usage                  | Matching Text Example          | Transformed Text Example       |
|------------------|----------------------------------------|--------------------------------|--------------------------------|--------------------------------|
| `@match->action` | Search and replace in incoming text    | `%d ". " @"_"->" " %s+->title` | `1. out_and_about`             | `1. Out and About`             |
| `..`             | Matches text between two other matches | `%d " - " ..->title '('`       | `1 - time out of joint (1959)` | `1 - Time Out of Joint (1959)` |


Positional Matches
------------------

| Form                      | Description                                                 | Example Usage            | Matching Text Example          | Transformed Text Example |
|---------------------------|-------------------------------------------------------------|--------------------------|--------------------------------|--------------------------|
| `$`                       | Matches the end of the filename                             | `.. %parens! $`          | `(2011) Quadrophenia (deluxe)` | `(2011) Quadrophenia`    |
| `^`                       | Matches the beginning of the filename                       | `((^|<<',') %c)*`        | `abracadabra`                  | `a,b,r,a,c,a,d,a,b,r,a`  |
| `%inparens`               | Matches text enclosed in parentheses                        | `@%inparens->'REDACTED'` | `Hung Up (radio mix)`          | `Hung Up (REDACTED)`     |
| `%inbraces`, `%incurlies` | Same, for `[]` and `{}`                                     |                          |                                |                          |
| `/regular-expression/`    | Positional features in regular expressions work as expected | `@/\bthe\b/i->upper`     | `The Anthem`                   | `THE Anthem`             |
