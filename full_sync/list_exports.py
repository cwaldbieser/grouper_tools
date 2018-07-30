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

def load_exports(db):
    """
    Generate exports group names.
    """
    query = dedent("""\
        SELECT NAME
        FROM grouper_groups_v
        WHERE TYPE_OF_GROUP = 'group'
        AND NAME LIKE 'app:%'
        and NAME LIKE '%:exports:%'
        ORDER BY NAME
        """)
    with closing(db.cursor()) as cursor:
        cursor.execute(query)
        for row in list(fetch_batch(cursor)):
            yield row[0]

def main(args):
    """
    Load group memberships for each group and emit line-JSON.
    """
    config = load_config()    
    mysql_opts = dict(config.items("MySQL"))
    if 'port' in mysql_opts:
        mysql_opts['port'] = int(mysql_opts['port'])
    with closing(db_conn_factory(mysql_opts)) as db:
        for group in load_exports(db):
            print(group)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get memberships for Grouper groups.")
    parser.add_argument(
        "-o",
        "--outfile",
        action="store",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Output file.")
    args = parser.parse_args()
    main(args)
