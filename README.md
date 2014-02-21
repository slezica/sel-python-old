# item

A powerful command-line replacement for cut.

# Simple

`item` has a dead simple syntax backed by sensible defaults:

    $ item 3 <<< "a b   c d   e"
    c

# Powerful

`item` understands multiple fields and field ranges:

    $ item 1 3:5 <<< "a b c d e"
    a c d e

even negative indexes, which are taken from the end:

    $ item -1 <<< "a b c d e"
    e

all the way to negative bounds for ranges:

    item 4:-1 <<< "a b c d e"
    d e

don't state the obvious:

# Flexible


