#! /bin/bash

PYTHON=/opt/python27/bin/python
FILTER_SSH_GROUPS=/home/grouper/full_sync/filter_ssh_groupmap.py
SYNCHRONIZE=/home/grouper/full_sync/synchronize.sh
LOG=/var/log/grouper_tools/full_sync.log
function tstamp
{
    date '+%Y-%m-%dT%H:%M:%S'
}

ALL_EXPORTS=$(mktemp)
/home/grouper/full_sync/list_export_groups > "$ALL_EXPORTS"

# Mailman
echo "["$(tstamp)"] Starting mailman group sync ..." >> "$LOG"
"$PYTHON" "$FILTER_SSH_GROUPS" /etc/grouper/provisioners/maillists/groupmap.json "$ALL_EXPORTS" | \
    "$SYNCHRONIZE" > /dev/null 2>> "$LOG"
echo >> "$LOG"

# Share-o-matic
echo "["$(tstamp)"] Starting share-o-matic group sync ..." >> "$LOG"
"$PYTHON" "$FILTER_SSH_GROUPS" /etc/grouper/provisioners/shareomatic/volume_its/groupmap.json "$ALL_EXPORTS" | \
    "$SYNCHRONIZE" > /dev/null 2>> "$LOG"
echo >> "$LOG"

# Zimbra distribution lists.
echo "["$(tstamp)"] Starting Zimbra distribution list group sync ..." >> "$LOG"
"$PYTHON" "$FILTER_SSH_GROUPS" /etc/grouper/provisioners/zimbra/groupmap.json "$ALL_EXPORTS" | \
    "$SYNCHRONIZE" > /dev/null 2>> "$LOG"
echo >> "$LOG"

# LDAP
echo "["$(tstamp)"] Starting LDAP group sync ..." >> "$LOG"
/home/grouper/full_sync/match_export_groups | \
    /home/grouper/full_sync/exclude_large_groups | \
        "$SYNCHRONIZE" > /dev/null 2>> "$LOG"
echo >> "$LOG"

# Board Effect (Workrooms)
# BE general access is already triggered during LDAP full sync.
echo "["$(tstamp)"] Starting Board Effect group sync ..." >> "$LOG"
/home/grouper/full_sync/list_be_workroom_groups.py | \
    "$SYNCHRONIZE" > /dev/null 2>> "$LOG"
echo >> "$LOG"

# Slack (UserGroups)
echo "["$(tstamp)"] Starting Slack group sync ..." >> "$LOG"
/home/grouper/full_sync/list_slack_usergroups.py | \
    "$SYNCHRONIZE" > /dev/null 2>> "$LOG"
echo >> "$LOG"

# o365
echo "["$(tstamp)"] Starting o365 group sync ..." >> "$LOG"
/home/grouper/full_sync/list_o365_groups.py | \
    "$SYNCHRONIZE" > /dev/null 2>> "$LOG"
echo >> "$LOG"


rm "$ALL_EXPORTS"

