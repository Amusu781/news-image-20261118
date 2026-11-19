#!/usr/bin/env python3
"""Draw the 18 November 2026 front page for THE DAILY WORLD.

A fresh, self-contained Pillow program. It renders a 1024x1024 newspaper
front page from the day's reported stories and saves it as entry.png
next to this file. Run:  python3 draw_frontpage.py
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (158, 28, 28)
NAVY = (24, 42, 74)
GREY = (90, 86, 76)
BLUE = (46, 110, 168)
GOLD = (214, 158, 40)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
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


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def draw_lead_art(draw, x, y, w, h):
    """Shenzhen skyline at dusk, an arriving jet and three summit flags."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    draw.ellipse([x + w - 72, y + 12, x + w - 28, y + 56], fill=GOLD)
    # skyline towers
    towers = [(0.00, 0.60, 0.17), (0.19, 0.40, 0.16), (0.37, 0.54, 0.17),
              (0.56, 0.32, 0.16), (0.74, 0.48, 0.16)]
    for fx, fh, fw in towers:
        tx = x + int(w * fx)
        tw = int(w * fw)
        th = int(h * fh)
        draw.rectangle([tx, y + h - th - 24, tx + tw, y + h - 24],
                       fill=NAVY)
        for wy in range(y + h - th - 14, y + h - 32, 13):
            for wx in range(tx + 5, tx + tw - 5, 11):
                draw.rectangle([wx, wy, wx + 4, wy + 5], fill=GOLD)
    # ground strip
    draw.rectangle([x, y + h - 24, x + w, y + h], fill=(64, 74, 60))
    # three flags standing in front of the towers
    for i in range(3):
        px = x + 22 + i * 92
        py = y + h - 108
        draw.rectangle([px, py, px + 4, y + h - 24], fill=(40, 40, 40))
        if i == 0:  # China
            draw.rectangle([px + 4, py, px + 62, py + 32], fill=(196, 30, 30))
            star(draw, px + 15, py + 11, 6, GOLD)
            star(draw, px + 29, py + 8, 3, GOLD)
            star(draw, px + 33, py + 16, 3, GOLD)
        elif i == 1:  # United States
            for s in range(7):
                c = (178, 34, 52) if s % 2 == 0 else (240, 240, 240)
                draw.rectangle([px + 4, py + s * 5, px + 62, py + s * 5 + 5],
                               fill=c)
            draw.rectangle([px + 4, py, px + 26, py + 17], fill=NAVY)
        else:  # Russia
            for s, c in enumerate([(240, 240, 240), (30, 90, 180),
                                   (200, 40, 40)]):
                draw.rectangle([px + 4, py + s * 11, px + 62,
                                py + s * 11 + 11], fill=c)


def story_block(draw, x, y, w, kicker, headline, body):
    """One story block in a grid column; returns y below the block."""
    f_kick = font(SANS_B, 15)
    f_head = font(SERIF_B, 25)
    f_body = font(SANS, 14)
    draw.rectangle([x, y + 2, x + 26, y + 6], fill=RED)
    draw.text((x, y + 12), kicker, font=f_kick, fill=RED)
    y2 = para(draw, x, y + 36, headline, f_head, w, 28)
    y2 = para(draw, x, y2 + 4, body, f_body, w, 18)
    return y2


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    L, R = 36, 988
    CW = R - L

    # ---- Masthead ----
    f_mast = font(SERIF_B, 84)
    title = "THE DAILY WORLD"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 18), title, font=f_mast, fill=INK)
    rule(d, L, R, 116, 3)
    f_date = font(SANS_B, 22)
    d.text((L, 128), "WEDNESDAY, 18 NOVEMBER 2026", font=f_date, fill=INK)
    tag = "ONE DAY  ·  SIX STORIES"
    d.text((R - d.textlength(tag, font=f_date), 128), tag,
           font=f_date, fill=RED)
    rule(d, L, R, 162, 1)

    # ---- Lead story ----
    y = 176
    f_kick = font(SANS_B, 18)
    d.text((L, y), "APEC  ·  SHENZHEN  —  LEAD STORY", font=f_kick, fill=RED)
    f_head = font(SERIF_B, 52)
    head = "XI GREETS TRUMP IN SHENZHEN"
    if d.textlength(head, font=f_head) > CW:
        f_head = font(SERIF_B, 46)
    d.text((L, 204), head, font=f_head, fill=INK)
    f_sub = font(SERIF, 26)
    d.text((L, 262), "Three-way talks with Putin set for Thursday",
           font=f_sub, fill=(60, 58, 50))
    lead_top = 300
    lead_h = 148
    body_w = 560
    f_body = font(SANS, 18)
    para(d, L, lead_top,
         "Xi Jinping personally greeted Donald Trump at the foot of Air "
         "Force One in Shenzhen \u2014 a first for any visiting leader \u2014 "
         "as APEC opened. Xi and Vladimir Putin met and both denounced "
         "Western protectionism and sanctions ahead of Thursday\u2019s "
         "three-way Xi\u2013Trump\u2013Putin talks. The US\u2013China tariff "
         "truce runs to 10 January 2027.",
         f_body, body_w, 24)
    draw_lead_art(d, L + body_w + 24, lead_top, CW - body_w - 24, lead_h)
    rule(d, L, R, lead_top + lead_h + 12, 3)

    # ---- Five story blocks: 3 columns x 2 rows ----
    col_w = (CW - 2 * 20) // 3
    xs = [L, L + col_w + 20, L + 2 * (col_w + 20)]
    row_y = lead_top + lead_h + 28
    row1 = [
        ("MIDDLE EAST  ·  GULF",
         "US jets strike Iran as Gulf war widens",
         "US jets hit a Revolutionary Guard missile site on Iran\u2019s "
         "Qeshm Island. Iran said it struck US forces in Kuwait and "
         "Bahrain; a UAE ship was hit in the Strait of Hormuz."),
        ("UKRAINE  ·  CRIMEA",
         "Crimea bridge destroyed",
         "Ukrainian drones and missiles destroyed the road bridge\u2019s "
         "central section, its arch crumbling into the sea \u2014 just "
         "before Putin meets Xi and Trump in China."),
        ("UNITED STATES  ·  SENATE",
         "Peltola wins Alaska; Democrats take Senate",
         "Mary Peltola defeated Republican incumbent Dan Sullivan in "
         "Alaska, giving Democrats a projected 56\u201344 majority in the "
         "incoming Senate."),
    ]
    ends = [story_block(d, xs[i], row_y, col_w, *row1[i]) for i in range(3)]
    row_y = max(ends) + 14
    rule(d, L, R, row_y - 6, 1)
    row2 = [
        ("ASIA  ·  WEATHER",
         "Cyclone Akvan nears India\u2019s coast",
         "Landfall is forecast on India\u2019s Andhra Pradesh coast around "
         "noon on Friday 20 November as a very severe cyclonic storm, "
         "winds 120\u2013130 km/h gusting to 145 km/h."),
        ("HEALTH",
         "US loses measles status; Ebola soars",
         "The US lost its measles elimination status after nearly three "
         "decades; Mexico and Bolivia lost it too. Ebola in DR Congo "
         "has more than doubled in three months to over 11,000 cases "
         "and 5,400 deaths."),
    ]
    ends = [story_block(d, xs[i], row_y, col_w, *row2[i]) for i in range(2)]
    # Also box in the third slot of row 2
    bx, by = xs[2], row_y
    bw, bh = col_w, 148
    d.rectangle([bx, by, bx + bw, by + bh], outline=INK, width=2)
    d.text((bx + 12, by + 10), "ALSO ON WEDNESDAY",
           font=font(SANS_B, 15), fill=RED)
    para(d, bx + 12, by + 36,
         "Canada\u2019s Mark Carney met Trump in Shenzhen as Canada\u2013US "
         "trade talks continue.",
         font(SANS, 16), bw - 24, 20)
    row_y = max(max(ends), by + bh) + 10

    # ---- Bottom ticker ----
    tick_y = 876
    d.rectangle([0, tick_y, W, 966], fill=NAVY)
    f_tick = font(SANS_B, 18)
    tick = ("QUAD LEADERS MEET IN MANILA \u2014 first leader-level meeting "
           "in over two years; Trump announces a major US\u2013Philippines "
           "trade deal  ·  GTA VI LAUNCHES AT MIDNIGHT after a 13-year "
           "wait  ·  RUBIO: no evidence of a \u201csystemic attack\u201d on "
           "the US capital  ·  MAGNITUDE 6 QUAKE hits Papua New Guinea  ·  "
           "MODI returns to Delhi after the ASEAN summit")
    ty = tick_y + 5
    for line in wrap(d, tick, f_tick, W - 48):
        d.text((24, ty), line, font=f_tick, fill=(255, 255, 255))
        ty += 21

    # ---- Footer ----
    f_foot = font(SANS, 15)
    foot = "THE DAILY WORLD  ·  WEDNESDAY 18 NOVEMBER 2026"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, 972), foot, font=f_foot, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
