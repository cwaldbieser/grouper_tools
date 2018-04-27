
from __future__ import print_function
import sys
sys.path.append("/opt/grouper_scripts")
from jython_grouper import *
import stem_walk 

def main():
    """
    Walk the "app" tree and search for groups in the "exports" folders.
    Print the name of those groups.
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
