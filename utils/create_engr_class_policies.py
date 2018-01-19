
from __future__ import print_function
import argparse
import sys
sys.path.append("/opt/grouper_scripts")
from jython_grouper import (
    addGroup,
    getGroup,
    getRootSession, 
)
import loader_tools
from edu.internet2.middleware.grouper.misc import CompositeType
from edu.internet2.middleware.grouper.privs import Privilege

CLASS_YEAR_SQL = """SELECT LOWER(SUBSTR(GOREMAL_EMAIL_ADDRESS, 0, INSTR(GOREMAL_EMAIL_ADDRESS, '@')-1)) subject_id, 'ldap' subject_source_id FROM ( SELECT A.sgbstdn_pidm, A.sgbstdn_stst_code, A.sgbstdn_acyr_code, A.sgbstdn_coll_code_1, A.sgbstdn_styp_code, A.sgbstdn_leav_from_date, A.sgbstdn_term_code_eff, A.stvterm_start_date, A.stvterm_end_date, ROW_NUMBER() OVER ( PARTITION BY A.sgbstdn_pidm ORDER BY A.stvterm_start_date DESC ) rn FROM ( SELECT Q.sgbstdn_pidm, Q.sgbstdn_stst_code, Q.sgbstdn_acyr_code, Q.sgbstdn_coll_code_1, Q.sgbstdn_styp_code, Q.sgbstdn_leav_from_date, Q.sgbstdn_term_code_eff, R.stvterm_start_date, R.stvterm_end_date FROM SGBSTDN Q INNER JOIN SATURN.STVTERM R ON Q.sgbstdn_term_code_eff = R.STVTERM_CODE WHERE ( TO_CHAR(stvterm_end_date,'YYYYMMDD') <= TO_CHAR(sysdate,'YYYYMMDD') OR TO_CHAR(sysdate,'YYYYMMDD') BETWEEN TO_CHAR(stvterm_start_date,'YYYYMMDD') AND TO_CHAR(stvterm_end_date,'YYYYMMDD') ) ) A ) B INNER JOIN goremal ON sgbstdn_pidm = GOREMAL_PIDM AND GOREMAL_EMAL_CODE = 'VXID' AND GOREMAL_STATUS_IND = 'A' WHERE rn = 1 AND sgbstdn_acyr_code = '{}' AND sgbstdn_stst_code IN ('AS','AF','AB','EX', 'GR') AND sgbstdn_coll_code_1 in ('01','02') AND sgbstdn_styp_code IN ('C','F','T','E', 'P')"""

ENGR_MAJORS = ['cee', 'chbe', 'ece', 'egrs', 'me']

def main(args):
    """
    Set the expiration times on a group for all subjects identfied in a file.
    """
    session = getRootSession()
    if args.create_class_ref:
        create_class_ref_group(session, args)
    if args.create_engr_ref:
        create_engr_ref_groups(session, args)
    if args.create_engr_spaces_pol:
        create_engineering_spaces_policies(session, args)

def create_class_ref_group(session, args):
    """
    Create the class year reference group.
    """
    global CLASS_YEAR_SQL
    year = args.year
    stem = 'ref:student'
    ext = "class{}".format(year)
    name = ext
    g = addGroup(session, stem, ext, name)
    print("Created group: {}".format(g.name))
    gname = g.name
    db_id = "hrlists"
    query = CLASS_YEAR_SQL.format(year)
    g = loader_tools.connect_group_to_sql_source(
        session,
        gname,
        db_id,
        query)
    print("Created loader job for: {}".format(g.name))

def create_engr_ref_groups(session, args):
    """
    Create Engneering reference groups for new class year.
    """
    global ENGR_DEGREES
    year = args.year
    viewers_g = getGroup(session, 'ref:engineering:etc:engr_ref_viewers')
    read_priv = list(Privilege.getInstances('read'))[0]
    stem = 'ref:student:class{}'.format(year)
    class_year_g = getGroup(session, stem)
    stem_prefix = 'ref:engineering'
    tags = list(ENGR_MAJORS)
    if not args.no_engu:
        tags.append('engu')
    for major in tags:
        stem = "ref:student:majors:major_{}".format(major)
        student_major_g = getGroup(session, stem)
        stem = "{}:{}".format(stem_prefix, major.upper())
        ext = "{}_{}".format(major, year)
        name = ext
        g = addGroup(session, stem, ext, name) 
        print("Created group: {}".format(g.name))
        g.assignCompositeMember(CompositeType.INTERSECTION, class_year_g, student_major_g)
        print("Transformed group `{}` into an intersection of `{}` AND `{}`".format(
            g.name, class_year_g.name, student_major_g.name))
        g.grantPriv(viewers_g.toSubject(), read_priv, False) 
        print("Granted READ priv on `{}` to `{}`.".format(
            g.name, viewers_g.name))

def create_engineering_spaces_policies(session, args):
    year = args.year
    disabled_g = getGroup(session, 'ref:disabled')
    tags = list(ENGR_MAJORS)
    if not args.no_engu:
        tags.append('engu')
    for major in tags:
        stem = 'app:spaces:engineering'
        ext = '{}_{}_students_allow'.format(major, year)
        name = '{} {} Students_allow'.format(major.upper(), year)
        allow_g = addGroup(session, stem, ext, name)
        print("Created ALLOW policy: `{}`".format(allow_g.name))
        ref_path = "ref:engineering:{}:{}_{}".format(
            major.upper(), major, year)
        ref_g = getGroup(session, ref_path) 
        allow_g.addMember(ref_g.toSubject())
        allow_g.store()
        print("Added `{}` as a member to `{}`.".format(ref_g.name, allow_g.name))
        ext = '{}_{}_students_deny'.format(major, year)
        name = '{} {} Students_deny'.format(major.upper(), year)
        deny_g = addGroup(session, stem, ext, name)
        print("Created DENY policy: `{}`".format(deny_g.name))
        deny_g.addMember(disabled_g.toSubject())
        deny_g.store()
        print("Added `{}` as a member to `{}`.".format(disabled_g.name, deny_g.name))
        stem = 'app:spaces:exports:engineering'
        ext = '{}_{}_students'.format(major, year)
        name = '{} {} Students'.format(major.upper(), year)
        pol_g = addGroup(session, stem, ext, name)
        print("Created policy: `{}`".format(pol_g.name))
        pol_g.assignCompositeMember(CompositeType.COMPLEMENT, allow_g, deny_g)
        print("Transformed `{}` into a complement of `{}` minus `{}`.".format(
            pol_g.name, allow_g.name, deny_g.name))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create engineering policies for a class year.")
    parser.add_argument(
        "year",
        action="store",
        type=int,
        help="The YYYY class year.")
    parser.add_argument(
        '-c',
        '--create-class-ref',
        action='store_true',
        help='Create the class year reference group and wire up a loader job.')
    parser.add_argument(
        '-e',
        '--create-engr-ref',
        action='store_true',
        help='Create the class year engineering reference groups.')
    parser.add_argument(
        '-E',
        '--create-engr-spaces-pol',
        action='store_true',
        help='Create the class year engineering policy groups for Spaces.')
    parser.add_argument(
        '--no-engu',
        action='store_true',
        help="Don't create ENGU policies or reference groups.")
    args = parser.parse_args()
    main(args)

