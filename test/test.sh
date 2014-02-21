if [[ ! $(which sel) ]]; then
    sel() {
        python sel.py "$@"
    }
    echo "Using python sel.py"
else
    echo "Using $(which sel)"
fi

test() {
    runcmd="$@"
    output=$($@)
    status=$?
}

fail() {
    echo "FAIL '$runcmd' $1"
}

status() {
    [ "$status" != "$1" ] && fail "expected status $1, exited with $status"
}

output() {
    [ "$output" != "$1" ] && fail "expected output '$1', got '$output'"
}

test sel 2>/dev/null
status 2

test sel 1 <<< "a b c"
status 0
output "a"

test sel -1 -2 <<< "a b c"
status 0
output "c b"

test sel 1:3 <<< "a b c d e"
status 0
output "a b c"

test sel 1:-1 <<< "a b c d e"
status 0
output "a b c d e"

test sel 2:-2 <<< "a b c d e"
status 0
output "b c d"

test sel --delim x 2 <<< "axbxc"
status 0
output "b"

test sel 2:3 --regex "[abc]" <<< "1a2b3c4"
status 0
output "2 3"

# CMD="item"
# echo "item"
# assert status 2 $?

# R=$(item 1 <<< "a b c" )
# assert output "a" "$R"

# # echo "a b c d e" | item 1:a2

# # echo "a b c d e" | item 1:2:3:4

# set -v
# echo "a b c d e" | item 1:2 3 -1