

from __future__ import print_function
import json
import sys
from jython_grouper import *

def main():
    """
    Read the `/etc/grouper/groupmap.json` file and produce a list of 
    Grouper groups that match the patterns.
    """
    # Swap STDERR and STDOUT
    stdout = sys.stdout
    stderr = sys.stderr
    sys.stdout = stderr
    sys.stderr = stdout
    session = getRootSession()
    with open("/etc/grouper/groupmap.json", "rb") as f:
        config = json.load(f)
    for k in config.keys():
        try:
            x = getGroups(session, k)
        except:
            continue
        for g in x:
            print(g.name)

if __name__ == "__main__":
    main()

