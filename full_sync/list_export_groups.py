
from __future__ import print_function
import sys
sys.path.append("/opt/grouper_scripts")
from jython_grouper import *
import stem_walk 

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
    # Main program
    session = getRootSession()
    for stem, sub_stems, groups in stem_walk.walk_stems(session, "app"):
        if stem.name.endswith(":exports"):
            for g in groups:
                print(g.name)

if __name__ == "__main__":
    main()
