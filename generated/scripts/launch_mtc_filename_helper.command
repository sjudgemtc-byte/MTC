#!/bin/zsh
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
/usr/bin/env python3 "$SCRIPT_DIR/mtc_filename_helper_app.py"
