"""Download finished Higgsfield images into output/<lead>/ads_raw/ and record their URLs in sources.json.
usage: python data/fetch_generated.py <lead_id> '<json {index: url}>'   (index 0 or "hero" -> hero.png)"""
import json, sys
from pathlib import Path
import httpx

lid, m = sys.argv[1], json.loads(sys.argv[2])
base = Path("output") / lid
(base / "ads_raw").mkdir(parents=True, exist_ok=True)
sp = base / "sources.json"
src = json.load(open(sp)) if sp.exists() else {}
for k, url in m.items():
    name = "hero" if str(k) in ("0", "hero") else f"ad_{int(k):02d}"
    out = base / "ads_raw" / f"{name}.png"
    if out.exists():
        out.rename(out.with_name(f"{name}_prev.png"))
    out.write_bytes(httpx.get(url, timeout=120, follow_redirects=True).content)
    src[name.replace("ad_", "").lstrip("0") or "hero"] = url
    print(name, out.stat().st_size)
json.dump(src, open(sp, "w"), indent=1)
