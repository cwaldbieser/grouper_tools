#! /bin/bash

THISDIR="$( cd $(dirname $0); pwd)"
SCRIPT="$THISDIR/$(basename $0)"
SYNC=/opt/grouper_tools/sync_group
GROUPS_LIST="${1:-$THISDIR/groups.txt}"

while read group <&3; do
    read -p  "About to sync group '$group'.  Press [Enter]."
    "$SYNC" "$group"
    echo ""
done 3< "$GROUPS_LIST"
