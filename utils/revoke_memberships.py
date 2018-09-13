
from __future__ import print_function
import argparse
import sys
sys.path.append("/opt/grouper_scripts")
from jython_grouper import (
    findSubject,
    getRootSession, 
    getGroup,
)
import subj_memberships
from edu.internet2.middleware.subject import SubjectNotFoundException

def main(args):
    """
    Remove subjects from a group. 
    """
    verbose = args.verbose
    group = args.group
    session = getRootSession() 
    for line in args.infile:
        subject_name = line.strip()
        try:
            subject = findSubject(subject_name)
        except SubjectNotFoundException as ex:
            print("[WARN] Subject '{}' was not found.".format(subject_name), file=sys.stderr)
            continue 
        memberships = list(subj_memberships.getMembershipsForSubject(session, subject))
        for m in memberships:
            g = m.getGroup()
            name = g.name
            if name == group:
                m.delete()
                g.store()
                print("Removed '{}' membership for subject '{}'.".format(group, subject_name))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove subjects from a group.")
    parser.add_argument(
        "group",
        action="store",
        help="The name of the group.")
    parser.add_argument(
        "infile",
        action="store",
        type=argparse.FileType("r"),
        help="Read subject IDs from INFILE (use '-' for STDIN).")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Be chatty.")
    args = parser.parse_args()
    main(args)

