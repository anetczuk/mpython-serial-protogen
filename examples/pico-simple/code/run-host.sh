#!/bin/bash

set -eu

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")


LIBDIR="$SCRIPT_DIR"

if [ ! -z ${PYTHONPATH+x} ]; then
	export PYTHONPATH=$PYTHONPATH:$SCRIPT_DIR:$LIBDIR
else
	export PYTHONPATH=$SCRIPT_DIR:$LIBDIR
fi


# cd $SCRIPT_DIR

python3 $SCRIPT_DIR/host/main.py $@
