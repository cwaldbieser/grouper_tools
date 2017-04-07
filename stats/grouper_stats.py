
from __future__ import print_function
import sys
sys.path.append("/opt/grouper_scripts")
from subjects import getPersonMembers
from stem_walk import walk_stems
from jython_grouper import getGroup, getStem, getRootSession

def count_child_stems(session, parent_stem_name):
    """
    Count the number of child stems.
    """
    parent_stem = getStem(session, parent_stem_name)
    count = 0
    for stem in parent_stem.getChildStems():
        count += 1
    return count
   
def count_groups(session, parent_stem_name):
    """
    Return the number of groups nested under `parent_stem_name`.
    """
    count = 0
    for stem, child_stems, groups in walk_stems(session, parent_stem_name):
        stem_name = stem.name
        parts = stem_name.split(':')
        if 'etc' in parts:
            continue
        for group in groups:
            count += 1
    return count 

def count_groups_members(session, parent_stem_name):
    """
    Return the number of person members of the groups nested under `parent_stem_name`.
    """
    subjects = set([])
    for stem, child_stems, groups in walk_stems(session, parent_stem_name):
        stem_name = stem.name
        parts = stem_name.split(':')
        if 'etc' in parts:
            continue
        for group in groups:
            for member in getPersonMembers(group):
                subjects.add(member)
    return len(subjects)

def count_group_members(session, group_name):
    """
    Count the number of person members in `group_name`.
    """
    return len(list(getPersonMembers(getGroup(session, group_name))))

def main():
    """
    Generate Grouper deployment statistics.
    """
    print("")
    session = getRootSession()
    print("Applications: {0}".format(count_child_stems(session, "app")))
    print("Bundles: {0}".format(count_child_stems(session, "bundle")))
    print("Reference Groups: {0}".format(count_groups(session, "ref")))
    print("Basis Groups: {0}".format(count_groups(session, "basis")))
    print("Students: {0}".format(count_group_members(session, "ref:student:students")))
    print("Employees: {0}".format(count_groups_members(session, "ref:employee")))
    print("Alumni w/ degree: {0}".format(count_group_members(session, "ref:alumni:alum_w_degree")))
    print("Alumni no degree: {0}".format(count_group_members(session, "ref:alumni:alum_no_degree")))
    print("Employee Services: {0}".format(count_group_members(session, "bundle:employee_services:employee_services")))

if __name__ == "__main__":
    main() 
