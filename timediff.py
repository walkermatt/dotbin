#!/usr/bin/python

"""Calculates the difference between two times
and print out the results

Usage:
  timediff.py [options] START_TIME END_TIME

Options:
  -h --help     Show this help message and exit

"""
from docopt import docopt
from datetime import datetime

def calc_diff(start, end):
    fmt = '%H:%M:%S'
    d = datetime.strptime(end, fmt) - datetime.strptime(start, fmt)
    hours, remainder = divmod(d.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return (hours, minutes, seconds)

if __name__ == '__main__':
    args = docopt(__doc__)

    try:
        start = args['START_TIME']
        end = args['END_TIME']
    except KeyError:
        print(__doc__)
        exit(1)

    print '%02d:%02d:%02d' % calc_diff(start, end)

