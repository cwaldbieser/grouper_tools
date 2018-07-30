#! /bin/bash

# Load config variables.
. /etc/grouper_tools/config.sh

# Set variables
THISDIR="$( cd $(dirname $0); pwd)"
SCRIPT="$THISDIR/$(basename $0)"
MAKE_MESSAGES="$THISDIR/get_members_for_groups"
TXQPRODUCER="/var/opt/txamqp_tools/txqproducer"
MAX_SUBJECTS_PER_GROUP=${MAX_SUBJECTS_PER_GROUP:-200}

if [ -z "$1" ]; then
    echo "Usage: $0 GROUP_NAMES_FILE" >&2
    exit 1
fi

"$MAKE_MESSAGES" "$1" --max-subjects "$MAX_SUBJECTS_PER_GROUP" | while read jsonstr; do
    echo "$jsonstr" | \
        "$TXQPRODUCER" "$GROUPER_EXCHANGE" "$ROUTE_KEY" - -e "$EXCHANGE_ENDPOINT" -u "$EXCHANGE_USER" --passwd-file "$EXCHANGE_PASSWD_FILE"
done
