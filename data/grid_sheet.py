"""Contact sheet with a 10% grid over each raw ad — for drawing protect boxes by eye."""
import sys
from PIL import Image, ImageDraw
lid, out, nums = sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3].split(",")]
W = 360
tiles = []
for n in nums:
    im = Image.open(f"output/{lid}/ads_raw/ad_{n:02d}.png").convert("RGB")
    im = im.resize((W, round(im.height * W / im.width)))
    d = ImageDraw.Draw(im)
    for i in range(1, 10):
        x = W * i / 10; y = im.height * i / 10
        c = (255, 0, 0) if i == 5 else (255, 80, 80)
        d.line([(x, 0), (x, im.height)], fill=c, width=1); d.line([(0, y), (W, y)], fill=c, width=1)
        d.text((x + 1, 1), str(i), fill=(255, 0, 0)); d.text((1, y + 1), str(i), fill=(255, 0, 0))
    d.text((4, 12), f"#{n}", fill=(0, 0, 255))
    tiles.append(im)
H = max(t.height for t in tiles)
sheet = Image.new("RGB", (len(tiles) * (W + 8), H), "white")
for k, t in enumerate(tiles):
    sheet.paste(t, (k * (W + 8), 0))
sheet.save(out)
