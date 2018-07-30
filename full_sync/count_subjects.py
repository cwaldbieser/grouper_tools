#! /usr/bin/env python

from __future__ import print_function
import argparse
from ConfigParser import SafeConfigParser
from contextlib import closing
import itertools
import json
import os
import os.path
import sys
from textwrap import dedent


def main(args):
    """
    Load group memberships for each group and emit line-JSON.
    """
    counter = 0
    for line in args.jsonl:
        doc = json.loads(line)
        subjects = doc.get('subjects', [])
        counter += len(subjects)
    print(counter)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count subjects in line-JSON data.")
    parser.add_argument(
        "jsonl",
        action="store",
        type=argparse.FileType("r"),
        help="File containing line-JSON data.  Use `-` for STDIN.")
    args = parser.parse_args()
    main(args)
