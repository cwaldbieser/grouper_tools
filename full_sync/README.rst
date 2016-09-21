============================
Full Synchronization Scripts
============================

`match_export_groups` is a shell wrapper front end that uses `gsh.jython`
to run the `match_export_groups.py` Jython script.  That script reads the
config file `/etc/grouper/groupmap.json` used by the LDAP provisioners
and extracts the group and stem patterns from it.  Each entry is checked
against Grouper and resolved to full path(s) of the group(s).

This list of groups is then fed to the `synchronize.sh` script, which can
read from STDIN (or a named file if an argument is provided) and calls on
the `sync_group` script from th ecore tools to synchronize each group.

The `synchronize_interactive.sh` group is similar, except it requires a
named file argument or it automatically selects a file named `groups.txt`.
It processes groups one at a time, asking the user to press "Enter" 
between each sync.

