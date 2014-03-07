from distutils.core import setup

setup(
    name     = 'sel',
    url      = 'http://github.com/slezica/sel',
    version  = '0.2.2',
    packages = ['sel'],
    scripts  = ['bin/sel'],

    author       = 'Santiago Lezica',
    author_email = 'slezica89@gmail.com',

    description = 'A field selection command-line tool',
)