#!/bin/bash

set -eu


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_NAME=`basename "$0"`


SRC_PATH="$SCRIPT_DIR/../../src/"

OUT_DIR="$SCRIPT_DIR/code"


mkdir -p "$OUT_DIR"


cd $SRC_PATH


## execute

python3 -m mpyserialprotogen --input_config "$SCRIPT_DIR/pico-protocol.json" --output_dir "$OUT_DIR" $@
