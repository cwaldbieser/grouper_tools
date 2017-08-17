
from __future__ import print_function
import argparse
import sys
sys.path.append("/opt/grouper_scripts")
from jython_grouper import getRootSession, getGroup
import temporal

def main(args):
    """
    Set the expiration times on a group for all subjects identfied in a file.
    """
    group = args.group
    session = getRootSession() 
    for line in args.infile:
        subject = line.strip()
        rval = temporal.setMembershipTime(session, group, subject, expire_str=args.expires)
        if not rval:
            print("Could not set membership time for subject '{0}'.".format(subject), file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set expiration times on a group for a list of subjects.")
    parser.add_argument(
        "group",
        action="store",
        help="The name of the group.")
    parser.add_argument(
        "expires",
        action="store",
        help="The expiration time in yyyy-mm-dd HH:MM:SS format.")
    parser.add_argument(
        "infile",
        action="store",
        type=argparse.FileType("r"),
        help="Read subject IDs from INFILE (use '-' for STDIN).")
    args = parser.parse_args()
    main(args)

