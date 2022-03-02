#!/usr/bin/env python3

import sys
import argparse
import re
import urllib.parse
from geomet import wkt as wkt_parser
import itertools
import unittest


def parse_bbox(line, frmt):
    line = line.strip()
    if frmt == 'URL':
        line = urllib.parse.unquote(line)
        match = re.search(r'BBOX=(\d+\.?\d+,\d+\.?\d+,\d+\.?\d+,\d+\.?\d+)', line, flags=re.IGNORECASE)
        if match:
            line = match.group(1)
    return line.strip().split(',')


def flattern_coords(coords):
    while True:
        if isinstance(coords[0][0], float):
            break
        coords = list(itertools.chain.from_iterable(coords))
    return coords


def bbox2wkt(bbox):
    x1, y1, x2, y2 = bbox
    wkt = f'POLYGON(({x1} {y1}, {x1} {y2}, {x2} {y2}, {x2} {y1}, {x1} {y1}))'
    return wkt


def wkt2bbox(wkt):
    geom = wkt_parser.loads(wkt.upper())
    coords = geom['coordinates']
    coords = flattern_coords(coords)
    xmin, ymin, xmax, ymax = [None, None, None, None]
    for ring in coords:
        # print(ring)
        for [x, y] in ring:
            if xmin is None or x < xmin:
                xmin = x
            if xmax is None or x > xmax:
                xmax = x
            if ymin is None or y < ymin:
                ymin = y
            if ymax is None or y > ymax:
                ymax = y
    return f'{xmin},{ymin},{xmax},{ymax}'


def cli():
    desc = "Transform WMS GetMap style BBOX value to WKT or WKT to BBOX"
    arg_parser = argparse.ArgumentParser(__file__, description=desc, argument_default=argparse.SUPPRESS)
    arg_parser.add_argument('--file', help='File containing BBOX or WKT values to convert, if no file is specified the BBOX or WKT is read from stdin')
    arg_parser.add_argument('--format', default="BBOX", help='Format being parsed, either BBOX (default), URL or WKT')
    args = vars(arg_parser.parse_args())
    format = args['format']
    with open(args['file']) if 'file' in args else sys.stdin as f:
        for num, line in enumerate(f, 1):
            if format in ['BBOX', 'URL']:
                try:
                    bbox = parse_bbox(line, format)
                    wkt = bbox2wkt(bbox)
                    print(wkt)
                except Exception as ex:
                    raise ValueError(f'Unable to parse BBOX, line: {num}, text: {line}') from ex
            elif format == 'WKT':
                try:
                    bbox = wkt2bbox(line)
                    print(bbox)
                except Exception as ex:
                    raise ValueError(f'Unable to parse WKT, line: {num}, text: {line}') from ex


class TestBbox(unittest.TestCase):
    def test_flattern_coords(self):
        self.assertEqual(flattern_coords([[30.0, 10.0], [10.0, 30.0], [40.0, 40.0]]), [
                         [30.0, 10.0], [10.0, 30.0], [40.0, 40.0]])
        self.assertEqual(
            flattern_coords(
                [[[30.0, 10.0],
                  [40.0, 40.0],
                  [20.0, 40.0],
                  [10.0, 20.0],
                  [30.0, 10.0]]]),
                [[30.0, 10.0],
                [40.0, 40.0],
                [20.0, 40.0],
                [10.0, 20.0],
                [30.0, 10.0]])
        self.assertEqual(
            flattern_coords(
                [[[30.0, 10.0],
                  [40.0, 40.0],
                  [20.0, 40.0],
                  [10.0, 20.0],
                  [30.0, 10.0]]]),
                [[30.0, 10.0],
                [40.0, 40.0],
                [20.0, 40.0],
                [10.0, 20.0],
                [30.0, 10.0]])
        self.assertEqual(
            flattern_coords(
                [[[35.0, 10.0],
                  [45.0, 45.0],
                  [15.0, 40.0],
                  [10.0, 20.0],
                  [35.0, 10.0]],
                 [[20.0, 30.0],
                  [35.0, 35.0],
                  [30.0, 20.0],
                  [20.0, 30.0]]]),
                [[35.0, 10.0],
                [45.0, 45.0],
                [15.0, 40.0],
                [10.0, 20.0],
                [35.0, 10.0],
                [20.0, 30.0],
                [35.0, 35.0],
                [30.0, 20.0],
                [20.0, 30.0]])
        self.assertEqual(
            flattern_coords(
                [[[[40.0, 40.0],
                   [20.0, 45.0],
                   [45.0, 30.0],
                   [40.0, 40.0]]],
                 [[[20.0, 35.0],
                   [10.0, 30.0],
                   [10.0, 10.0],
                   [30.0, 5.0],
                   [45.0, 20.0],
                   [20.0, 35.0]],
                  [[30.0, 20.0],
                   [20.0, 15.0],
                   [20.0, 25.0],
                   [30.0, 20.0]]]]),
                [[40.0, 40.0],
                [20.0, 45.0],
                [45.0, 30.0],
                [40.0, 40.0],
                [20.0, 35.0],
                [10.0, 30.0],
                [10.0, 10.0],
                [30.0, 5.0],
                [45.0, 20.0],
                [20.0, 35.0],
                [30.0, 20.0],
                [20.0, 15.0],
                [20.0, 25.0],
                [30.0, 20.0]])


if __name__ == '__main__':
    cli()
