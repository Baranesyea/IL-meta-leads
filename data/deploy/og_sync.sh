#!/bin/sh
# Pull the link-preview files (public/og, public/s) and ClientPitch.jsx into the Base44 sandbox (/app) at commit $1.
# Slugs come as $2.. ; run from /app.
H=$1; shift
B=https://raw.githubusercontent.com/baranesyea/IL-meta-leads/$H/web/base44
curl -sfL -o src/pages/ClientPitch.jsx "$B/src/pages/ClientPitch.jsx" || echo "FAIL ClientPitch"
for s in "$@"; do
  for f in public/og/$s.jpg public/s/$s.html; do curl -sfL -o "$f" --create-dirs "$B/$f" || echo "FAIL $f"; done
done
rm -rf public/s/probe public/s/probe2.html
ls public/og | wc -l; ls public/s | wc -l
