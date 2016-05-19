
=============
Grouper Tools
=============

This collection of scripts act as wrappers and simple tools, designed to work
with the Lafayette College Grouper provisioning architecture.

The shell scripts included in this collection have user configurable
variables for paths to external tools, configuration files, etc.

-----------
Get Members
-----------

Example::

    $ $GROUPER_HOME/bin/gsh.jython get_members.py 'test:orkz:ldap_exports:nobz'

----------------------------
Sync Provisioners to Grouper
----------------------------

Sometimes the memberships of your external systems get ou of sync with what
Grouper says they ought to be.  This can happen for various reasons.
This script queries Grouper for what the actual membership ought to look like,
and then it notifies a provisioner delivery service to inform all the 
relevant downstream provisioners.

The downstream provisioners need to be able to interpret the final message and
make sure the services they interact with match the authoratative roster.

Example::

    ./sync_group 'test:orkz:ldap_exports:nobz'

Depends on the 'txamqp_tools` scripts.

