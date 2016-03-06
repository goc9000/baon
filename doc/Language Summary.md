BAON
====

(C) Copyright 2012-present Cristian Dinu (<goc9000@gmail.com>); Licensed under the GPLv3.


----------------

WORK IN PROGRESS

----------------


Language Summary
================


Pattern Matches
---------------

| Form                  | Description                             | Example   | Text Examples                | Text Counterexamples                |
|-----------------------|-----------------------------------------|-----------|------------------------------|-------------------------------------|
| `'text'` or `"text"`  | Matches that exact text                 | `'abc'`   | `abc`                        | `AbC` `def` `ab`                    |
| `%d`                  | Matches a number                        | `%d`      | `123` `0012`                 | `notanumber` `-4`                   |
| `%Nd`                 | Matches a number with N digits          | `%4d`     | `4567` `0123`                | `123` `123456` `notanumber`         |
| `%s`                  | Matches a single word or compound word  | `%s`      | `the` `quick` `12`  `pop-up` | `abc def`                           |
| `%Ns`                 | Matches a single word of N letters      | `%3s`     | `the` `123` `abc`            | `abcd` `12` `a b`                   |
| `%c`                  | Matches any single character            | `%c`      | `a` `b` `1` `2` `_`          | N/A (only end of filename)          |
| `%Nc`                 | Matches next N characters               | `%4c`     | `abcd` `1234` `ab c`         | `a` `12`                            |
| `%ws`                 | Matches any amount of whitespace        | `%ws`     | `_` `___` (empty text)       | `abc`                               |
| `%parens`             | Matches parentheses and the text within | `%parens` | `(1984)` `(remix)`           | `abc` `[1984]` `(())` `extra(text)` |
| `%braces`, `%curlies` | Same, for `[]` and `{}`                 |           |                              |                                     |
| `%path`               | Matches a path up to a basename         | `%path`   | `abc\def\gh` `abc/d e/f`     | `123`                               |
