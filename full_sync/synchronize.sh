#! /bin/bash

THISDIR="$( cd $(dirname $0); pwd)"
SCRIPT="$THISDIR/$(basename $0)"
SYNC=/opt/grouper_tools/sync_group

# If a file argument was provided, redirect the file to STDIN.
# Otherwise, this script reads from STDIN
if [ ! -z "$1" ]; then
   exec < "$1"
fi

while read group ; do
    "$SYNC" "$group"
done

