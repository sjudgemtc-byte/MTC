#!/bin/zsh
cd "$(dirname "$0")"
(sleep 1; open "http://127.0.0.1:8765") &
"/Users/simonjudge/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3" app.py
