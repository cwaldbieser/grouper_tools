
from __future__ import print_function
import argparse
import sys
sys.path.append("/opt/grouper_scripts")
from jython_grouper import (
    addGroup,
    getGroup,
    getGroups,
    getRootSession, 
)
from edu.internet2.middleware.grouper.misc import CompositeType
from edu.internet2.middleware.grouper import exception as gexcept

def main(args):
    reset_policies = args.reset_policies
    use_display_extension = args.use_display_extension
    org_type = 'dept'
    club = args.club
    if club:
        org_type = 'club'
    list_pols = args.list_policies
    session = getRootSession()
    emp_ref = getGroup(session, "ref:employee:employee")
    disabled_ref = getGroup(session, "ref:disabled")
    basis_stem = 'app:ems:hr_tk_policies:basis'
    policy_stem = 'app:ems:hr_tk_policies'
    exports_stem = 'app:ems:exports:hrtk'
    depts = []
    for grp in getGroups(session, "app:ems:ref:{}:".format(org_type)):
        ext = grp.extension
        display_ext = grp.displayExtension
        if not club:
            nodept_ext = ext[5:]
        else:
            nodept_ext = ext
        allow_name = '{}_allow'.format(nodept_ext)
        deny_name = '{}_deny'.format(nodept_ext)
        emp_name = '{}_emp'.format(ext)
        if not club:
            emp_grp = get_group(session, basis_stem, emp_name)
            if emp_grp is None:
                print("Creating '{}:{}' ...".format(basis_stem, emp_name))
                emp_grp = addGroup(session, basis_stem, emp_name, emp_name)
                emp_grp.assignCompositeMember(CompositeType.INTERSECTION, grp, emp_ref)
        allow_pol = get_group(session, policy_stem, allow_name)
        exists = allow_pol is not None
        if not exists:
            print("Creating '{}:{}' ...".format(policy_stem, allow_name))
            allow_pol = addGroup(session, policy_stem, allow_name, allow_name)
        if (not exists) or reset_policies:
            print("Setting policy for '{}:{}' ...".format(policy_stem, allow_name))
            if exists:
                remove_members(allow_pol)
            if club:
                allow_pol.addMember(grp.toSubject())
            else:
                allow_pol.addMember(emp_grp.toSubject())
        deny_pol = get_group(session, policy_stem, deny_name)
        exists = deny_pol is not None
        if not exists:
            print("Creating '{}:{}' ...".format(policy_stem, deny_name))
            deny_pol = addGroup(session, policy_stem, deny_name, deny_name)
        if (not exists) or reset_policies:
            print("Setting policy for '{}:{}' ...".format(policy_stem, deny_name))
            if exists:
                remove_members(deny_pol)
            deny_pol.addMember(disabled_ref.toSubject())
        policy = get_group(session, exports_stem, nodept_ext)
        if policy is None:
            print("Creating '{}:{}' ...".format(exports_stem, nodept_ext))
            policy = addGroup(session, exports_stem, nodept_ext, nodept_ext)
            policy.assignCompositeMember(CompositeType.COMPLEMENT, allow_pol, deny_pol)
        if use_display_extension:
            print("Updating description for '{}:{}' to '{}' ...".format(exports_stem, nodept_ext, display_ext))
            policy.description = display_ext
            policy.store()
        if list_pols:
            print(policy.name)

def remove_members(g):
    for m in list(g.members):
        try:
            g.deleteMember(m)
        except gexcept.MemberDeleteAlreadyDeletedException as ex:
            pass
 
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create EMS policies.")
    parser.add_argument(
        '-l',
        '--list-policies',
        action='store_true',
        help="List policies.")
    parser.add_argument(
        "-c",
        "--club",
        action='store_true',
        help='Process student organizations instead of departments.')
    parser.add_argument(
        "-x",
        "--use-display-extension",
        action='store_true',
        help='Populate the policy description with the reference group display extension.')
    parser.add_argument(
        "-r",
        "--reset-policies",
        action='store_true',
        help='Reset existing policies to their default memberships.')
    args = parser.parse_args()
    main(args)

