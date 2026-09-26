"""Rendered ads at phone width (390px) in rows — for review. usage: <lead_id> <out_prefix>"""
import sys
from PIL import Image, ImageDraw
lid, pre = sys.argv[1], sys.argv[2]
for part, rng in (("a", range(1, 11)), ("b", range(11, 21))):
    ims = []
    for n in rng:
        im = Image.open(f"output/{lid}/ads/ad_{n:02d}.png").convert("RGB")
        ims.append((n, im.resize((390, round(im.height * 390 / im.width)))))
    rows = [ims[:5], ims[5:]]
    H = sum(max(i.height for _, i in r) + 10 for r in rows)
    W = Image.new("RGB", (5 * 400, H), "white"); d = ImageDraw.Draw(W); y = 0
    for r in rows:
        for k, (n, im) in enumerate(r):
            W.paste(im, (k * 400, y)); d.text((k * 400 + 4, y + 4), str(n), fill="red")
        y += max(i.height for _, i in r) + 10
    W.save(f"{pre}_{part}.png")
