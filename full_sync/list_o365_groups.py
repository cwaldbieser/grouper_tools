#! /usr/bin/env python

from __future__ import print_function
import ConfigParser
import json

def main():
    scp = ConfigParser.SafeConfigParser()
    scp.read(["/etc/txamqpprovisioners/provisioners/o365/o365_subjects.cfg"])
    provision_group = scp.get("PROVISIONER", "provision_group") 
    print(provision_group)
    with open("/etc/txamqpprovisioners/provisioners/o365/o365_group_map.json", "r") as f:
        doc = json.load(f)
    for group in doc:
        print(group)

if __name__ == "__main__":
    main()
