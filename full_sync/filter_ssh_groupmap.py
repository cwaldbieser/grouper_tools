#! /usr/bin/env python

from __future__ import print_function
import argparse
import json
import re

def main(args):
    """
    Filter a list of groups based on a regex group map.
    """
    doc = json.load(args.groupmap)
    pats = []
    for patstring, template in doc:
        if patstring == ".*":
            continue
        pat = re.compile(patstring)
        pats.append(pat)
    for group in args.infile:
        group = group.rstrip()
        for pat in pats:
            m = pat.search(group)
            if not m is None:
                print(group)
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test service ticket validation.")
    parser.add_argument(
        "groupmap",
        type=argparse.FileType("r"),
        action="store",
        help="The groupmap file to parse.")
    parser.add_argument(
        "infile",
        type=argparse.FileType("r"),
        action="store",
        help="The input file of group names to test.  Use '-' for STDIN.")
    args = parser.parse_args()
    main(args)

