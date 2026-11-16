import os, sys
from PIL import Image, ImageDraw

RES = sys.argv[1] if len(sys.argv) > 1 else "android/app/src/main/res"
BG = (91, 63, 209)
FG = (255, 255, 255)
S = 4  # supersampling for smooth edges


def wheel(size, radius_ratio, transparent):
    big = size * S
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0) if transparent else BG + (255,))
    d = ImageDraw.Draw(img)
    c = big / 2
    R = big * radius_ratio
    w = max(2, int(big * 0.07))
    r = R * 0.28
    d.ellipse([c - R, c - R, c + R, c + R], outline=FG, width=w)
    d.ellipse([c - r, c - r, c + r, c + r], fill=FG)
    d.line([c - R + w / 2, c, c - r, c], fill=FG, width=w)
    d.line([c + r, c, c + R - w / 2, c], fill=FG, width=w)
    d.line([c, c + r, c, c + R - w / 2], fill=FG, width=w)
    return img.resize((size, size), Image.LANCZOS)


SIZES = {"mdpi": (48, 108), "hdpi": (72, 162), "xhdpi": (96, 216), "xxhdpi": (144, 324), "xxxhdpi": (192, 432)}

for dens, (launcher, foreground) in SIZES.items():
    folder = os.path.join(RES, "mipmap-" + dens)
    if not os.path.isdir(folder):
        continue
    square = wheel(launcher, 0.34, False)
    square.save(os.path.join(folder, "ic_launcher.png"))
    mask = Image.new("L", (launcher, launcher), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, launcher - 1, launcher - 1], fill=255)
    rounded = Image.new("RGBA", (launcher, launcher), (0, 0, 0, 0))
    rounded.paste(square, (0, 0), mask)
    rounded.save(os.path.join(folder, "ic_launcher_round.png"))
    wheel(foreground, 0.22, True).save(os.path.join(folder, "ic_launcher_foreground.png"))

values = os.path.join(RES, "values")
if os.path.isdir(values):
    with open(os.path.join(values, "ic_launcher_background.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#5B3FD1</color>\n</resources>\n')
print("icons done")
