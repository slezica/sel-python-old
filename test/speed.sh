for _ in {1..1000}; do ps aux; done > test_data

echo -n 'Timing cut'

time {
    cat test_data | cut -d ' ' -f 1-4 > /dev/null
}

echo -en '\nTiming sel'

time {
    cat test_data | python sel.py 1:4 > /dev/null
}

rm test_data