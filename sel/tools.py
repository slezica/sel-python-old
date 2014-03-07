import itertools, re

def is_numeric(string):
    try   : return int(string) and True
    except: return False

def is_range(string):
    return string.count(':') == 1

def is_blank(string):
    return len(string.strip()) > 0

def getitem(lst, i, default = None):
    try   : return lst[i]
    except: return default

def flatten(fields):
    """ Flattens [1, 2, [3, 4], 5] into [1, 2, 3, 4, 5]. """
    listified = (rg if isinstance(rg, list) else [rg] for rg in fields)
    return itertools.chain(*listified)


def parse_selector(arg):
    if is_numeric(arg):
        number = int(arg)
        return number - 1 if number > 0 else number

    if is_range(arg):
        first, last = [int(i) if i else None for i in arg.split(':')]

        # Ranges begin at 1 and are right-inclusive
        if first: first -= 1
        if last and last < 0: last = (last + 1) or None

        return slice(first, last)

    # If it's just a string, it'll be taken for a column name
    return arg

def default_split(line):
    return line.split()

def make_delim_split(delimiter):
    def split(line):
        return line.split(delimiter)

    return split

def make_regex_split(pattern):
    regex = re.compile(pattern)
        
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


def file_by_lines(file):
    # An open stdin cannot be iterated with `for..in...`, it will hang
    # waiting for stdin to get an EOF.
    # We replace it with a line iterable.
    while True:
        line = file.readline()
        if line:
            yield line
        else:
            break