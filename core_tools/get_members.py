
import argparse
import sys
from jython_grouper import *


def main(args):
    group_name = args.group_path
    session = getRootSession()
    group = getGroup(session, group_name)
    for subj in group.getMembers():
        sys.stderr.write(subj.getSubjectId())
        sys.stderr.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Grouper group members")
    parser.add_argument(
        "group_path",
        action="store",
        help="The full path to the Grouper group.")
    args = parser.parse_args()
    main(args)

