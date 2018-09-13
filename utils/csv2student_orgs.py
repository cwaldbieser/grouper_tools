

from __future__ import print_function
import argparse
import csv
import re
import sys
sys.path.append("/opt/grouper_scripts")
from jython_grouper import (
    addGroup,
    findSubject,
    getGroup,
    getRootSession, 
)
from edu.internet2.middleware.grouper import exception as gexcept

def main(args):
    dry_run = args.dry_run
    reader = csv.DictReader(args.csv_file)
    groups = {}
    for row in reader:
        club = row['Club']
        club_id = normalize_org(row['Club'])
        email = row['Email']
        netid = email.lower().replace("@lafayette.edu", "")
        info = groups.setdefault(club_id, {})
        info['desc'] = club
        members = info.setdefault('members', set([]))
        members.add(netid)
    keys = groups.keys()
    keys.sort()
    session = None
    if not dry_run:
        session = getRootSession()
    for group_id in keys:
        group_path = "app:ems:ref:club:{}".format(group_id)
        info = groups[group_id]
        print("{}: {}".format(group_path, info['desc']))
        if not dry_run:
            create_ref_group(session, group_id, info) 
        members = list(info['members'])
        for member in members:
            print("  {}".format(member))

def create_ref_group(session, group_id, info):
    stem = "app:ems:ref:club"
    desc = info['desc']
    g = get_group(session, stem, group_id)
    if g is None:
        g = addGroup(session, stem, group_id, desc)
    members = info['members']
    existing = list(g.members)
    existing_set = set([])
    for memb in existing:
        subj = memb.getSubject()
        if subj.sourceId != "ldap":
            continue
        subj_id = subj.name.lower()
        existing_set.add(subj_id)
    to_add = members - existing_set
    to_remove = existing_set - members
    for subj in to_add:
        subj = findSubject(subj)
        g.addMember(subj)
    for subj in to_remove:
        subj = findSubject(subj)
        g.deleteMember(subj)

def get_group(session, stem, extension):
    """
    Returns group or None.
    """
    gname = "{}:{}".format(stem, extension)
    try:
        g = getGroup(session, gname)
    except gexcept.GroupNotFoundException as ex:
        return None
    return g

def normalize_org(org):
    org = org.lower()
    org = ' '.join(org.split())
    org = org.replace(" ", "_")
    org = re.sub('[^a-zA-Z_]', '', org) 
    return org

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create student organization reference groups for EMS from CSV data.")
    parser.add_argument(
        'csv_file',
        type=argparse.FileType("r"),
        help="CSV file to import (use - for STDIN).")
    parser.add_argument(
        "-d",
        "--dry-run",
        action='store_true',
        help="Print the groups that would be created; don't actually create reference groups.")
    args = parser.parse_args()
    main(args)

