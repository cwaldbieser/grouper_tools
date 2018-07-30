#! /bin/bash

THISDIR="$( cd $(dirname $0); pwd)"
PYTHON=/opt/python27/bin/python
SYNC_GROUPS="$THISDIR/sync_groups.sh"
EXCLUDE_GROUPS="$THISDIR/exclude_groups"
LIST_EXPORTS="$THISDIR/list_exports"
LOG=/var/log/grouper_tools/full_sync.log

function tstamp
{
    date '+%Y-%m-%dT%H:%M:%S'
}

echo "[$(tstamp)][INFO] Starting exports sync ..." > "$LOG"
"$LIST_EXPORTS" | "$EXCLUDE_GROUPS" | "$SYNC_GROUPS" -
echo "[$(tstamp)][INFO] Starting exports sync ..." >> "$LOG"



