import sys, itertools
import cli

from tools import getitem, flatten, is_blank, file_by_lines


def main():
    conf = cli.parse()

    if isinstance(conf.input, file):
        conf.input = file_by_lines(conf.input)
    
    # Columns specified by name require special treatment after we open
    # our input stream.
    by_name = [(i, f) for i, f in enumerate(conf.fields) if isinstance(f, str)]

    if by_name:
        headline = conf.input.next()
        headers  = conf.splitf(headline)
        indexed  = { name: i for i, name in enumerate(headers) }

        for i, name in by_name:
            if name not in indexed:
                raise Exception()

            conf.fields[i] = indexed[name]

        # Push the headline back. Dirty, but not that dirty
        conf.input = itertools.chain([headline], conf.input)

    if not conf.headers:
        conf.input.next()

    if not conf.fields:
        conf.fields = [slice(None)]

    conf.printf(sel(conf.input, conf.fields, conf.splitf))


def sel(input, indexes, splitf):
    """ Performs the cutting and selecting
        input  : an iterable of lines
        indexes: an iterable of valid list indexes (int, slices)
        splitf : the function used to separate indexes in input
    """ 

    for line in input:
        fields   = filter(is_blank, splitf(line))
        selected = (getitem(fields, i, default = '') for i in indexes)
        yield flatten(selected)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)