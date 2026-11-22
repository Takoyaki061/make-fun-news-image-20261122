#!/usr/bin/env python3
"""Draw the 22 November 2026 front page (1024x1024 PNG, deterministic).

Run: python3 draw-news-image-20261122.py [out.png]
Writes entry.png next to this script by default. Uses PIL only, fixed
seed, no timestamps, no network. Every string is baked into the pixels.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)      # warm newsprint
INK = (20, 22, 26)           # near-black
ACCENT = (200, 50, 30)       # signal red
SEA = (176, 205, 224)        # gulf water
LAND = (227, 217, 190)       # land fill
SECONDARY = (58, 58, 52)     # dark grey for captions

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, xy, text, fnt, fill, spacing=2):
    """Draw text with manual letter tracking (PIL has no tracking)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing
    return x


def draw_gulf_map(draw, box):
    """Schematic Persian Gulf map: sea, land, Bahrain marked red."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=LAND, outline=INK, width=2)
    # Sea: a narrow diagonal band across the panel (the Gulf).
    sea = [
        (x0 + 70, y0 + 18), (x1 - 25, y0 + 55), (x1 - 50, y0 + 130),
        (x0 + 250, y0 + 185), (x0 + 140, y0 + 115),
    ]
    draw.polygon(sea, fill=SEA, outline=(90, 120, 150))
    # Qatar peninsula nub on the south shore.
    draw.polygon([(x0 + 280, y0 + 165), (x0 + 310, y0 + 150),
                  (x0 + 322, y0 + 175), (x0 + 292, y0 + 188)], fill=LAND)
    # Bahrain: red dot + ring, mid-Gulf on the western shore.
    bx, by = x0 + 205, y0 + 145
    draw.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=ACCENT,
                 outline=INK, width=2)
    draw.ellipse([bx - 24, by - 24, bx + 24, by + 24], outline=ACCENT, width=2)
    # Labels.
    draw.text((x0 + 18, y0 + 10), "IRAN", font=SANS_B(26), fill=INK)
    draw.text((x0 + 18, y0 + 186), "SAUDI", font=SANS_B(26), fill=INK)
    draw.text((x0 + 18, y0 + 212), "ARABIA", font=SANS_B(26), fill=INK)
    draw.text((x0 + 245, y0 + 118), "BAHRAIN", font=SANS_B(28), fill=ACCENT)
    draw.text((x0 + 245, y0 + 148), "al-Riffa - Awali", font=SANS(24), fill=INK)
    draw.text((x0 + 330, y0 + 45), "PERSIAN", font=SANS_B(24), fill=(40, 70, 95))
    draw.text((x0 + 330, y0 + 71), "GULF", font=SANS_B(24), fill=(40, 70, 95))


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    title = "THE WORLD TODAY"
    tf = SERIF_B(76)
    d.text(((W - d.textlength(title, font=tf)) / 2, 16), title, font=tf, fill=INK)
    d.line([(40, 106), (984, 106)], fill=INK, width=3)
    # Date strip.
    tracked(d, (40, 118), "SUNDAY 22 NOVEMBER 2026", SANS_B(32), ACCENT, 2)
    right = "WORLD EDITION"
    d.text((984 - d.textlength(right, font=SANS_B(32)), 118), right,
           font=SANS_B(32), fill=INK)
    d.line([(40, 160), (984, 160)], fill=INK, width=2)

    # ---- Lead story (left column) ---------------------------------------
    LX, LW = 40, 552
    y = 178
    tracked(d, (LX, y), "GULF ESCALATION", SANS_B(28), ACCENT, 3)
    y += 44
    headline = "IRGC says it hit US Patriot radars in Bahrain"
    for line in wrap(d, headline, SERIF_B(56), LW):
        d.text((LX, y), line, font=SERIF_B(56), fill=INK)
        y += 66
    y += 6
    deck = ("Tehran claims missiles and drones struck two US air-defence "
            "radars at al-Riffa and Awali. Bahrain says an Iranian attack "
            "set a civilian site on fire. No casualties; "
            "the US has not confirmed damage.")
    for line in wrap(d, deck, SANS(30), LW):
        d.text((LX, y), line, font=SANS(30), fill=INK)
        y += 38
    y += 12
    # Map panel.
    map_box = (LX, y, LX + LW, y + 240)
    draw_gulf_map(d, map_box)
    y = map_box[3] + 10
    for line in wrap(d, "Schematic map - not to scale. The two bases sit "
                        "on Bahrain's Gulf coast.", SANS(26), LW):
        d.text((LX, y), line, font=SANS(26), fill=SECONDARY)
        y += 32

    # ---- Right rail: three briefs ---------------------------------------
    RX, RW = 624, 360
    d.line([(604, 178), (604, 984)], fill=INK, width=2)
    y = 178

    def brief(kicker, head, deck_lines, head_size=34, deck_size=26):
        nonlocal y
        tracked(d, (RX, y), kicker, SANS_B(26), ACCENT, 2)
        y += 38
        hf = SERIF_B(head_size)
        for line in wrap(d, head, hf, RW):
            d.text((RX, y), line, font=hf, fill=INK)
            y += head_size + 10
        y += 4
        df = SANS(deck_size)
        for line in deck_lines:
            for sub in wrap(d, line, df, RW):
                d.text((RX, y), sub, font=df, fill=INK)
                y += deck_size + 8
        y += 8

    brief("CLIMATE - ANTALYA",
          "COP31 tables new text after overtime",
          ["Approval due Sunday;",
           "fossil-fuel wording disputed."])
    d.line([(RX, y), (RX + RW, y)], fill=INK, width=1)
    y += 14
    brief("FRANCE",
          "Fourth weekend of cost-of-living protests",
          ["Nationwide marches over rising prices",
           "enter a fourth straight weekend."])
    d.line([(RX, y), (RX + RW, y)], fill=INK, width=1)
    y += 14
    # Myanmar brief: big magnitude numeral as the anchor.
    tracked(d, (RX, y), "MYANMAR", SANS_B(26), ACCENT, 2)
    y += 38
    d.text((RX, y), "4.1", font=SERIF_B(84), fill=INK)
    d.text((RX + 160, y + 46), "magnitude", font=SANS_B(28), fill=INK)
    d.text((RX + 160, y + 78), "quake", font=SERIF_B(34), fill=INK)
    y += 116
    for line in wrap(d, "Early-Sunday tremor, per India's NCS.",
                     SANS(26), RW):
        d.text((RX, y), line, font=SANS(26), fill=INK)
        y += 34

    # ---- Footer ---------------------------------------------------------
    d.line([(40, 990), (984, 990)], fill=INK, width=2)
    foot = "Sources: Reuters - Al Jazeera - ANI - The Paris Eye - NCS"
    d.text((40, 996), foot, font=SANS(24), fill=SECONDARY)

    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
