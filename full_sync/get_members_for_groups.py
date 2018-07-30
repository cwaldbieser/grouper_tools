#! /usr/bin/env python

from __future__ import print_function
import argparse
from ConfigParser import SafeConfigParser
from contextlib import closing
import itertools
import json
import os
import os.path
import sys
from textwrap import dedent
import MySQLdb

def fetch_batch(cursor, batch_size=None, **kwds):
    """
    Generator fetches batches of rows from the database cursor.
    """
    if batch_size is None:
        batch_size = cursor.arraysize
    while True:
        rows = cursor.fetchmany(batch_size)
        if len(rows) == 0:
            break
        for row in rows:
            yield row

def db_conn_factory(conn_info):
    return MySQLdb.connect(**conn_info)
    
def load_config():
    """
    Load configuration.
    """
    syspath = "/etc/grouppy/get_members.cfg"
    userpath = os.path.expanduser("~/.grouppy/get_members.cfg")
    config = SafeConfigParser()
    files = config.read([syspath, userpath])
    if len(files) == 0:
        raise Exception("No configuration could be found!")
    return config

def get_members(db, group):
    """
    """
    query = dedent("""\
        SELECT SUBJECT_ID
        FROM grouper_memberships_v
        WHERE GROUP_NAME = %s
        AND SUBJECT_SOURCE = 'ldap'
        AND list_type = 'list'
        """)
    with closing(db.cursor()) as cursor:
        cursor.execute(query, [group])
        members = list(fetch_batch(cursor))
    members = [row[0] for row in members]
    return members

def main(args):
    """
    Load group memberships for each group and emit line-JSON.
    """
    max_subjects = args.max_subjects
    config = load_config()    
    mysql_opts = dict(config.items("MySQL"))
    if 'port' in mysql_opts:
        mysql_opts['port'] = int(mysql_opts['port'])
    with closing(db_conn_factory(mysql_opts)) as db:
        for line in args.group_file:
            group = line.strip()
            if group == "":
                continue
            members = get_members(db, group)
            if max_subjects and len(members) > max_subjects:
                continue
            doc = {'group': group, 'subjects': members}
            sdata = json.dumps(doc)
            print(sdata, file=args.outfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get memberships for Grouper groups.")
    parser.add_argument(
        "group_file",
        action="store",
        type=argparse.FileType("r"),
        help="File containing group paths, one per line.  Use `-` for STDIN.")
    parser.add_argument(
        "-o",
        "--outfile",
        action="store",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="File containing group paths, one per line.  Use `-` for STDIN.")
    parser.add_argument(
        "--max-subjects",
        action="store",
        type=int,
        help="If group contains more members that MAX-SUBJECTS, do not output it.")
    args = parser.parse_args()
    main(args)
