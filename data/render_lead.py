"""Render the Hebrew overlays for one lead: python data/render_lead.py <lead_id>"""
import json, sys
sys.path.insert(0, ".")
from src.overlay import render_lead
p = f"data/leads/{sys.argv[1]}.json"
lead = json.load(open(p))
render_lead(lead)
json.dump(lead, open(p, "w"), ensure_ascii=False, indent=1)
for a in lead["new_ads"]:
    r = a["layout"]["render"]
    print(a["ad_no"], r["direction"], a["layout"]["rendered_zone"], r["ink"], r["scrim"])
