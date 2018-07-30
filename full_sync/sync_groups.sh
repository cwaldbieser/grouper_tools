#! /bin/bash

# Load config variables.
. /etc/grouper_tools/config.sh

# Set variables
THISDIR="$( cd $(dirname $0); pwd)"
SCRIPT="$THISDIR/$(basename $0)"
MAKE_MESSAGES="$THISDIR/get_members_for_groups"
TXQPRODUCER="/var/opt/txamqp_tools/txqproducer"
MAX_SUBJECTS_PER_GROUP=${MAX_SUBJECTS_PER_GROUP:-200}

function tstamp
{
    date '+%Y-%m-%dT%H:%M:%S'
}

if [ -z "$1" ]; then
    echo "Usage: $0 GROUP_NAMES_FILE" >&2
    exit 1
fi

TEMP_JSON=$(mktemp)
if "$MAKE_MESSAGES" "$1" --max-subjects "$MAX_SUBJECTS_PER_GROUP" > "$TEMP_JSON"; then

    while read jsonstr; do
        echo "$jsonstr" | \
            "$TXQPRODUCER" "$GROUPER_EXCHANGE" "$ROUTE_KEY" - -e "$EXCHANGE_ENDPOINT" -u "$EXCHANGE_USER" --passwd-file "$EXCHANGE_PASSWD_FILE"
    done < "$TEMP_JSON"
    rm "$TEMP_JSON"
else
    echo "[$(tstamp)][ERROR] Error looking up group memberships."
    rm "$TEMP_JSON"
fi

