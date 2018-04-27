#! /usr/bin/env python

from __future__ import print_function
import json

def main():
    with open("/etc/txamqpprovisioners/provisioners/board-effect/workroom_map.json", "r") as f:
        doc = json.load(f)
    for group in doc:
        print(group)

if __name__ == "__main__":
    main()
