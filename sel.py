#!/usr/bin/env python
import sys, itertools, argparse, re

# -----
# TOOLS
# -----

def flatten(fields):
    """ Flattens [1, 2, [3, 4], 5] into [1, 2, 3, 4, 5]. """
    listified = (rg if isinstance(rg, list) else [rg] for rg in fields)
    return itertools.chain(*listified)

def is_blank(string):
    return len(string.strip()) > 0

def getitem(lst, i, default = None):
    return lst[i] if isinstance(i, slice) or len(lst) > i else default

def int_or_none(value):
    return int(value) if value else None

# -------------
# MAIN FUNCTION
# -------------

def work(input, indexes, splitf):
    """ Performs the cutting and selecting
        input  : an iterable of lines
        indexes: an iterable of valid list indexes (int, slices)
        splitf : the function used to separate fields in input
    """ 

    for line in input:
        fields   = filter(is_blank, splitf(line))
        selected = (getitem(fields, i, '') for i in indexes)
        yield flatten(selected)

# ----------------------
# COMMAND-LINE INTERFACE
# ----------------------

def read_field(arg):
    """ Reads and returns an integer or slice.
        Indeces begin at 1 and slices are right-inclusive.
    """
    try:
        if ':' in arg:
            first, last = [int(i) if i else None for i in arg.split(':', 1)]
            if first: first -= 1
            if last < 0: last = (last + 1) or None
            return slice(first, last)
            
        else:
            index = int(arg)
            return index - 1 if index > 0 else index

    except Exception as e:
        raise argparse.ArgumentTypeError(
            "Improper format in field '%s' (%s)" % (arg, e)
        )


def default_split(line):
    return line.split()

def make_delim_split(delimiter):
    # This acts as type factory for argparse
    def split(line):
        return line.split(delimiter)

    return split

def make_regex_split(pattern):
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


def default_print(results):
    for result in results:
        print ' '.join(result).strip()


def aligned_print(results):
    results  = list(map(list, results)) # Read entire input
    columns  = zip(*results) # Not evident, but zip() transposes 2d-lists
    colsizes = [max(map(len, column)) for column in columns]

    for result in results:
        for i, field in enumerate(result):
            print '%-*s' % (colsizes[i], field),
        print



def run():
    parser = argparse.ArgumentParser(description='Extract fields from columns in input')

    parser.add_argument('fields',
        metavar ='field',
        type    = read_field,
        nargs   = '*',
        help    = 'integer indexes or first:last ranges'
    )

    parser.add_argument('-r', '--regex',
        type = make_regex_split,
        help = "delimit fields with a regular expression"
    )

    parser.add_argument('-d', '--delim',
        type = make_delim_split,
        help = "delimit fields with a string"
    )

    parser.add_argument('-f', '--file',
        help = "take input from file instead of stdin"
    )

    parser.add_argument('-s', '--skip-headers',
        action = 'store_true',
        help   = "skip the first line, assuming it's a table header"
    )

    parser.add_argument('-a', '--align',
        action = 'store_const',
        const  = aligned_print,
        help   = "aligns columns (buffers input)"
    )

    parser.add_argument('-c', '--cols',
        metavar = 'column',
        nargs   = '+',
        help    = 'select columns by names (assumes header on input)'
    )

    # parser.add_argument('-j', '--join',
    #     metavar = 'join',
    #     nargs   = '?',
    #     help    = 'string to join output fields with (default: --delim or space)'
    # )

    args = parser.parse_args()

    input   = open(args.file) if args.file else sys.stdin
    splitf  = args.regex or args.delim or default_split
    fields  = args.fields
    printf  = args.align or default_print
    
    if args.cols:
        headline = input.next()
        headers  = splitf(headline)
        indexed  = { name: i for i, name in enumerate(headers) }
        fields  += [indexed[name] for name in args.cols if name in indexed]

        # Push the headline back. Dirty, but not that dirty
        input = itertools.chain([headline], input)

    if args.skip_headers:
        input.next()

    if not fields:
        parser.print_usage()
        print 'No fields, ranges or columns selected'
        sys.exit(2)

    results = work(input, fields, splitf)

    try:
        printf(results)
    except IOError:
        pass

if __name__ == '__main__':
    run()