
import sys
sys.path.append("/opt/grouper_scripts")
from jython_grouper import getRootSession
import privs
import stem_walk

def main():
    """
    Walk the "app" tree and remove any individual subject permissions.
    """
    subjectSourceId = "ldap"
    root_stem = "lc:app"
    session = getRootSession()
    for astem, stems, groups in stem_walk.walk_stems(session, root_stem):
        for stem in stems:
           privs.revokeStemPrivBySubjectSourceId(session, stem.name, subjectSourceId)
        for group in groups:
            privs.revokeGroupPrivBySubjectSourceId(session, group.name, subjectSourceId, privName="admin")
            privs.revokeGroupPrivBySubjectSourceId(session, group.name, subjectSourceId, privName="read")

if __name__ == "__main__":
    main()

