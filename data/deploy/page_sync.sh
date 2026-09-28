#!/bin/sh
# Pull one client page into the Base44 sandbox (/app) from GitHub raw at commit $1.
# usage (from /app): sh page_sync.sh <hash> <folder> <PageName> <files in public/reports/<folder>...>
H=$1; D=$2; P=$3; shift 3
B=https://raw.githubusercontent.com/baranesyea/IL-meta-leads/$H/web/base44
for f in src/pages/$P.jsx src/App.jsx src/reports/data.js; do curl -sfL -o "$f" --create-dirs "$B/$f" || echo "FAIL $f"; done
for n in "$@"; do f=public/reports/$D/$n; curl -sfL -o "$f" --create-dirs "$B/$f" || echo "FAIL $f"; done
ls public/reports/$D | wc -l
grep -c "$D" src/reports/data.js src/App.jsx
