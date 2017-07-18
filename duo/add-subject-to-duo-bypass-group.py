#! /var/opt/internet2/grouper/grouper.apiBinary/bin/gsh.jython

from __future__ import print_function
import datetime
import sys
from jython_grouper import (
    findSubject,
    getRootSession, 
    getGroup 
)
sys.path.append("/opt/grouper_scripts")
import temporal

def usage():
    print("Usage: {0} SUBJECT".format(sys.argv[0]), file=sys.stderr)

def main(subject):
    group_name = "app:duo:ref:bypass"
    session = getRootSession()
    g = getGroup(session, group_name)
    s = findSubject(subject)
    if s:
        g.addMember(s)
    now = datetime.datetime.today()
    dt = datetime.timedelta(days=1) + now
    temporal.setMembershipTime(session, group_name, subject, expire_str=dt.strftime("%Y-%m-%d %H:%M:%S")) 

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    main(sys.argv[1])
