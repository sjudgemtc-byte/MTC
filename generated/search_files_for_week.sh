#!/bin/zsh

set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "Usage: $0 YYYY-MM-DD YYYY-MM-DD [search_root]"
  echo "Example: $0 2026-01-19 2026-01-23 /Users/simonjudge/Documents/MTC"
  exit 1
fi

start_date="$1"
end_date="$2"
search_root="${3:-/Users/simonjudge/Documents/MTC}"

end_exclusive=$(date -j -v+1d -f "%Y-%m-%d" "$end_date" "+%Y-%m-%d")

echo "Searching:"
echo "  Root: $search_root"
echo "  From: $start_date 00:00"
echo "  To:   $end_date 23:59"
echo

find "$search_root" -type f -newermt "$start_date 00:00" ! -newermt "$end_exclusive 00:00" | sort
