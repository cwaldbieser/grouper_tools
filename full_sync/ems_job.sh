#! /bin/bash

THISDIR="$( cd $(dirname $0); pwd)"
PYTHON=/opt/python27/bin/python
SYNC_GROUPS="$THISDIR/sync_groups.sh"
POLICIES=/home/grouper/full_sync/ems_policies.txt
LOG=/var/log/grouper_tools/ems_sync.log
function tstamp
{
    date '+%Y-%m-%dT%H:%M:%S'
}

#Clear log
> "$LOG"

echo "[$(tstamp)][INFO] Starting EMS sync job." >> "$LOG"
"$SYNC_GROUPS" "$POLICIES" >> "$LOG" 2>&1
echo "[$(tstamp)][INFO] Ended EMS sync job." >> "$LOG"
