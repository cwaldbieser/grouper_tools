
from __future__ import print_function
import json
import sys
from jython_grouper import *

def main():
    """
    Read the `/etc/txamqpprovisioners/groupmap.json` file and produce a list of 
    Grouper groups that match the patterns.
    """
    # Swap STDERR and STDOUT
    stdout = sys.stdout
    stderr = sys.stderr
    sys.stdout = stderr
    sys.stderr = stdout
    session = getRootSession()
    with open("/etc/txamqpprovisioners/ldap/groupmap.json", "rb") as f:
        config = json.load(f)
    for k in config.keys():
        try:
            x = getGroups(session, k)
        except:
            continue
        if k.endswith(":"):
            is_stem = True
        else:
            is_stem = False    
        for g in x:
            name = g.name
            if not is_stem:
                if k != name:
                    continue
            print(name)

if __name__ == "__main__":
    main()
