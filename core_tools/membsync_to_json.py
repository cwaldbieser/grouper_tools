#! /usr/bin/env python

from __future__ import print_function
import json
import sys

def main(argv):
    if len(argv) != 1:
        usage()
        sys.exit(1)
    group = argv[0]
    subjects = []
    for line in sys.stdin:
        subject = line.rstrip()
        subjects.append(subject)
    doc = {'group': group, 'subjects': subjects}
    json.dump(doc, sys.stdout)

def usage():
    print("Usage: {0} GROUPER_GROUP".format(sys.argv[0], file=sys.stderr))

if __name__ == "__main__":
    argv = sys.argv[1:]
    main(argv)
