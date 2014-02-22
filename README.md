# sel

`sel` is an inline field selection and table transformation tool
that aims to replace `cut`.


## Simple

Selecting a field from a line requires a single character:

    $ echo a b c d e | sel 3
    c


`sel` understands field ranges, in python style:

    $ echo "a b c d e" | sel 2:4
    b c d

    $ echo "a b c d e" | sel 2:-2
    b c d

    $ echo "a b c d e" | sel 3:
    c d e


## Flexible

By default, `sel` splits the input on whitespace. It can also
use a custom string or regular expression:

    $ cat users.csv
    1241,Bob
    3192,MitM
    3255,Alice

    $ cat users.csv | sel 1 --delim ,
    1241
    3192
    3255
    
    $ echo 1a2b3c4d | sel --regex [a-z] 2:3
    2 3


## Powerful

`sel` works well on multiline input, and can take advantage
of table headers if present. It can also produce tabular outputs.

    $ ps aux | sel 1 --skip-header
    root
    user1
    user2

    $ ps aux | sel --align --cols %MEM PID COMMAND 
    PID  COMMAND                          %MEM
    2414 /opt/google/chrome/chrome        1.7 
    5272 /opt/sublime_text_2/sublime_text 1.6 
    4662 /usr/bin/python3                 1.5 
    2470 /opt/google/chrome/chrome        1.5 
