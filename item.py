#!/usr/bin/env python
import sys, itertools, functools, argparse, re

# -----
# TOOLS
# -----

def flatten(ranges):
    """ Flattens [1, 2, [3, 4], 5] into [1, 2, 3, 4, 5]. """
    listified = (rg if isinstance(rg, list) else [rg] for rg in ranges)
    return itertools.chain(*listified)

def clean(strings):
    """ Removes blank strings from an iterable. """
    return filter(len, map(str.strip, strings))


# -----------
# ENTRY POINT
# -----------

def main(input, ranges, split):
    """ Performs the cutting and printing
        input : a file-like stream
        ranges: an iterable of valid list indexes (inc. slices)
        split : the function used to separate items in input
    """
    for line in input:
        items = clean(split(line))
        print ' '.join(flatten(items[i] for i in ranges))



def read_range(arg):
    """ Reads and returns an integer or slice.
        Note that our slices are right-inclusive.
    """
    try:
        if ':' in arg:
            bounds     = map(int, arg.split(':'))
            bounds[0] -= 1
            return slice(*bounds)
            
        else:
            index = int(arg)
            return index - 1 if index > 0 else index

    except Exception as e:
        raise argparse.ArgumentTypeError(
            "Improper format in range '%s' (%s)" % (arg, e)
        )


def default_split(line):
    return line.split()

def delim_split(delimiter):
    # This acts as type factory for argparse
    def split(line):
        return line.split(delimiter)

    return split

def regex_split(pattern):
    try:
        regex = re.compile(pattern)

    except Exception as e:
        raise argparse.ArgumentTypeError(
            "Invalid regular expression '%s'" % (pattern)
        )
        
    # This separates regex parsing from application and provides
    # a nice type factory for argparse
    def split(line):
        return regex.split(line)

    return split


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract items from columns in input')

    parser.add_argument('ranges',
        metavar ='range',
        type    = read_range,
        nargs   = '+',
        help    = 'integer indexes or start:end:step ranges'
    )

    parser.add_argument('-r', '--regex',
        type  = regex_split,
        help  = "delimit items with a regular expression"
    )

    parser.add_argument('-d', '--delim',
        type  = delim_split,
        help  = "delimit items with a string"
    )

    parser.add_argument('-f', '--file',
        help = "take input from file instead of stdin"
    )

    parser.add_argument('-s', '--skip-header',
        action = 'store_true',
        help   = "skip the first line, assuming it's a table header"
    )


    args = parser.parse_args()

    input  = open(args.file) if args.file else sys.stdin
    split  = args.regex or args.delim or default_split
    ranges = args.ranges
    
    if args.skip_header: input.readline()

    main(input, ranges, split)