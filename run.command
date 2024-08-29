#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$SCRIPT_DIR"

chmod +x "$SCRIPT_DIR/main"

"$SCRIPT_DIR/main"