#! /bin/bash

# Set variables
THISDIR="$( cd $(dirname $0); pwd)"
SCRIPT="$THISDIR/$(basename $0)"
export GROUPER_HOME=/opt/internet2/grouper/grouper.apiBinary
GSH_JYTHON="$GROUPER_HOME/bin/gsh.jython"

# Run script via `gsh.jython`
# Swap STDOUT and STDERR to get rid of gsh/Grouper preamble.
"$GSH_JYTHON" "$THISDIR/grouper_stats.py" "$@" 
