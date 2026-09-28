#!/bin/sh
# Pull the Ali Karim page files into the Base44 sandbox (/app) from GitHub raw at commit $1.
H=$1
B=https://raw.githubusercontent.com/baranesyea/IL-meta-leads/$H/web/base44
for f in src/pages/AliKarim.jsx src/App.jsx src/reports/data.js; do curl -sfL -o "$f" --create-dirs "$B/$f" || echo "FAIL $f"; done
for n in cur_01 cur_02 cur_03 cur_04 hero hero_m lp_00 lp_03 lp_08 lp_11 raw_01 raw_02 raw_03 raw_04 raw_05 raw_06 raw_07 raw_08 raw_09 raw_10 raw_11 raw_12 raw_13 raw_14 raw_15 raw_16 raw_17 raw_18 raw_19 raw_20; do
  f=public/reports/alikarim/$n.webp; curl -sfL -o "$f" --create-dirs "$B/$f" || echo "FAIL $f"
done
ls public/reports/alikarim | wc -l
grep -c alikarim src/reports/data.js src/App.jsx
