#!/usr/bin/env python
from os.path import exists
import sys
import xml.etree.ElementTree as ET
import re
import os.path

def print_counters(source):
    print('line-rate: ' + counter(source, 'LINE'))
    print('branch-rate: ' + counter(source, 'BRANCH'))
    print('complexity: ' + counter(source, 'COMPLEXITY', sum))


def fraction(covered, missed):
    return covered / (covered + missed)


def sum(covered, missed):
    return covered + missed


def counter(source, type, operation=fraction):
    cs = source.findall('counter')
    c = next((ct for ct in cs if ct.attrib.get('type') == type), None)

    if c is not None:
        covered = float(c.attrib['covered'])
        missed = float(c.attrib['missed'])

        return str(operation(covered, missed) * 100)
    else:
        return '0.0'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: printcover.py FILENAME")
        sys.exit(1)

    filename = sys.argv[1]
    source_roots = sys.argv[2:] if 2 < len(sys.argv) else '.'
    
    if filename == '-':
        root = ET.fromstring(sys.stdin.read())
    else:
        tree = ET.parse(filename)
        root = tree.getroot()

    print_counters(root)

