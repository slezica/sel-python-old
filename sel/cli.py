import sys, argparse
import tools

class Conf(object):
    def __init__(self, selectors, splitf, printf, headers, filename = None):
        self.input  = open(filename) if filename else sys.stdin
        self.fields = map(tools.parse_selector, selectors)

        self.splitf = {
            'regex'  : tools.make_regex_split,
            'delim'  : tools.make_delim_split,
            'default': lambda _: tools.default_split
        }[splitf[0]](splitf[1])

        self.printf = {
            'aligned': tools.aligned_print,
            'default': tools.default_print
        }[printf]

        self.headers = headers

    def __str__(self):
        return str(self.__dict__)


parser = argparse.ArgumentParser(description='Extract columns from input')

parser.add_argument('selectors',
    metavar ='selector',
    nargs   = '+',
    help    = 'integer indexes or first:last ranges'
)

parser.add_argument('-r', '--regex',
    type = lambda regex: ('regex', regex),
    help = "delimit columns with a regular expression"
)

parser.add_argument('-d', '--delim',
    type = lambda delim: ('delim', delim),
    help = "delimit columns with a string"
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
    const  = 'aligned',
    help   = "aligns columns (buffers input)"
)

parser.add_argument('-c', '--cols',
    metavar = 'column',
    nargs   = '+',
    help    = 'select columns by names (assumes header on input)'
)

parser.add_argument('-j', '--join',
    metavar = 'join',
    nargs   = '?',
    help    = 'string to join output fields with (default: --delim or space)'
)

def parse():
    args, extra = parser.parse_known_args()

    return Conf(
        filename  = args.file,
        splitf    = args.regex or args.delim or ('default', None),
        printf    = args.align or 'default',
        headers   = not args.skip_headers,
        selectors = args.selectors + extra,
    )

if __name__ == '__main__':
    print parse()