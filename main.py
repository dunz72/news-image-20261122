#!/usr/bin/env python3
"""The World in One Day - Sunday 22 November 2026.

A one-page newspaper front page (1024x1024) summarising 45 real world-news
stories from Sunday 22 November 2026. Drawn entirely with PIL primitives:
flat pastel editorial illustrations, a stylised world map with numbered
pins, and two-column briefs. Original code written for the make.fun
news-image-20261122 bounty.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 30                      # page margin
CW = W - 2 * M              # content width

PAPER = (246, 240, 224)
INK = (28, 26, 22)
MUTED = (96, 88, 74)
RULE = (60, 54, 44)
RED = (179, 64, 46)
BLUE = (46, 94, 140)
GREEN = (62, 122, 78)
AMBER = (176, 126, 30)
PURPLE = (107, 78, 142)
TEAL = (46, 122, 116)
BROWN = (140, 90, 46)
PANEL = (239, 231, 210)
MAP_BG = (233, 224, 198)
LAND = (198, 205, 178)

FD = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

def text_w(t, font):
    return d.textlength(t, font=font)

def wrap(t, font, maxw):
    lines, cur = [], ""
    for word in t.split():
        trial = (cur + " " + word).strip()
        if text_w(trial, font) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def draw_lines(x, y, lines, font, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def centered(y, t, font, fill):
    d.text(((W - text_w(t, font)) / 2, y), t, font=font, fill=fill)

def rule(y, x0=M, x1=W - M, w=2, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)

def letterspaced_centered(y, t, font, fill, gap=4):
    widths = [text_w(c, font) for c in t]
    total = sum(widths) + gap * (len(t) - 1)
    x = (W - total) / 2
    for ch, wd in zip(t, widths):
        d.text((x, y), ch, font=font, fill=fill)
        x += wd + gap

# ---------------------------------------------------------------- stories
# (num, headline, deck, category, colour) -- heroes 1-3, features 4-13
HEROES = [
    (1, "COP31 COLLAPSES WITH NO DEAL",
     "Antalya talks end without consensus as the EU rejects a draft with no fossil-fuel exit.",
     "CLIMATE", GREEN, "ANTALYA, TURKEY"),
    (2, "IRAN HITS TANKERS AT HORMUZ",
     "Three tankers struck; Bahrain says two hurt as US bases are hit and Houthis fire on Saudi.",
     "CONFLICT", RED, "STRAIT OF HORMUZ"),
    (3, "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
     "First trilateral summit yields a nuclear-risk declaration \u2014 but no Ukraine breakthrough.",
     "DIPLOMACY", BLUE, "SHENZHEN, CHINA"),
]
FEATURES = [
    (4, "MEXICO CAPTURES \u2018EL CHAPO ISIDRO\u2019",
     "11 killed in the Sinaloa raid on an FBI most-wanted cartel boss.", "CONFLICT", RED),
    (5, "COURT: MYANMAR COMMITTED GENOCIDE",
     "ICJ rules on the Rohingya \u2014 a first genocide verdict against a state.", "DIPLOMACY", BLUE),
    (6, "KYIV FLAT HIT; 14 FEARED TRAPPED",
     "Drone strike wrecks an apartment block; missile kills two in Kryvyi Rih.", "CONFLICT", RED),
    (7, "STOCKS SLIDE INTO CORRECTION",
     "S&P 500 falls 3.7% as the AI sell-off spreads to Asia.", "MARKETS", AMBER),
    (8, "EU\u2013INDONESIA SIGN TRADE DEAL",
     "A decade of talks ends; tariffs scrapped on up to 98.5% of goods.", "DIPLOMACY", BLUE),
    (9, "BEPICOLOMBO REACHES MERCURY",
     "Eight-year voyage ends in orbit around the innermost planet.", "SCIENCE", PURPLE),
    (10, "6.7 QUAKE SHAKES PERU\u2019S ANDES",
     "Lima rattled; cinemas evacuated, no casualties reported.", "DISASTER", BROWN),
    (11, "FACTORY FIRE: 3 DEAD, 50 MISSING",
     "Blaze sweeps a candy plant in Banten; rescuers search the ruins.", "DISASTER", BROWN),
    (12, "SEOUL MINISTER QUITS OVER AI CHEATING",
     "Exam scandal erupts days before Korea\u2019s college entrance test.", "POLITICS", TEAL),
    (13, "FBI CRIME DATABASE HACKED",
     "Trump confirms breach of the NCIC system of fingerprints and warrants.", "TECH", PURPLE),
]
BRIEFS = [
    (14, "Gaza strikes continue despite ceasefire framework; aid vehicle hit"),
    (15, "Hezbollah refuses to disarm as Israel keeps up pressure on Lebanon"),
    (16, "China\u2013Japan ties sour over Taiwan and critical minerals"),
    (17, "Spain heads to 29 Nov vote with PP and Vox on 190 seats in polls"),
    (18, "France: sixth Saturday of cost-of-living protests, turnout down 22%"),
    (19, "Estonia to shut Russian border as Moscow threatens a response"),
    (20, "Russian missiles land in Poland during drills nearby"),
    (21, "Hegseth memo curbs US\u2013Canada defence relationship"),
    (22, "Denmark expels Russian attach\u00e9 over alleged plot"),
    (23, "Russian cargo ship ablaze in Gulf of Finland after drone strike"),
    (24, "Ukrainian strikes damage the Crimean Bridge"),
    (25, "Saudi coalition downs Houthi missiles aimed at Riyadh"),
    (26, "US lead over China in Asia smallest since 2018, Lowy finds"),
    (27, "Amazon nears $7.5bn deal for Israeli AI start-up Decart"),
    (28, "UK opinion turns against Brexit, new polling suggests"),
    (29, "GTA 6 sets $3.79bn launch-day record"),
    (30, "Hunger Games prequel heads for $120m opening weekend"),
    (31, "Leeds stun Chelsea 4\u20131, first win at Stamford Bridge since 1999"),
    (32, "Man City held by Fulham; Arsenal draw 2\u20132 at Newcastle"),
    (33, "Gukesh defends chess crown as youngest title match opens in Geneva"),
    (34, "Bolsonaro moved to intensive care in Bras\u00edlia hospital"),
    (35, "Boat capsizes in Nigeria; 24 funeral mourners dead"),
    (36, "Bangladesh: garment strikes close 80 factories amid protests"),
    (37, "Pakistan says 15 militants killed in Mastung operations"),
    (38, "China renews UN bid to blacklist BLA and Majeed Brigade"),
    (39, "Sri Lanka top court clears organised-crime bill"),
    (40, "EU budget plan: \u20ac1.58tn, a 10.2% cut, plus 3% digital levy"),
    (41, "Saudi benchmark slides below 10,000, down 1.95%"),
    (42, "Belgium faces air-traffic halt in Monday strike"),
    (43, "Indonesia returns to ICAO Council for a 13th term"),
    (44, "China approves 6G pilots in eight regions"),
    (45, "Lewis Pugh swims 15 km across the Strait of Hormuz"),
]
# map pins: num -> (x, y, colour)
PINS = {
    1: (592, 668, GREEN), 2: (650, 676, RED), 3: (803, 680, BLUE),
    4: (209, 677, RED), 5: (508, 650, BLUE), 6: (566, 646, RED),
    7: (285, 658, AMBER), 8: (782, 706, BLUE), 9: (930, 646, PURPLE),
    10: (295, 712, BROWN), 11: (806, 718, BROWN), 12: (838, 666, TEAL),
    13: (255, 671, PURPLE),
}

# ---------------------------------------------------------------- top bar
f_top = SANS_B(13)
d.text((M, 16), "SUNDAY, 22 NOVEMBER 2026", font=f_top, fill=INK)
rt = "PRICE: FREE  \u00b7  45 STORIES  \u00b7  SIX CONTINENTS"
d.text((W - M - text_w(rt, f_top), 16), rt, font=f_top, fill=INK)
rule(40)

# ---------------------------------------------------------------- masthead
centered(50, "THE DAY IN WORLD NEWS", SERIF_B(56), INK)
letterspaced_centered(118, "45 STORIES \u00b7 6 CONTINENTS \u00b7 ONE DAY",
                      SANS_B(15), RED, gap=5)
# thin rules flanking the subhead
sub_w = text_w("45 STORIES \u00b7 6 CONTINENTS \u00b7 ONE DAY", SANS_B(15)) + 5 * 37
rule(128, M, (W - sub_w) / 2 - 16, 1)
rule(128, (W + sub_w) / 2 + 16, W - M, 1)
centered(140, "The World in One Day \u2014 Sunday 22 November 2026",
         SERIF(20), MUTED)
rule(170, w=3)

# ---------------------------------------------------------------- hero illustrations
def hero_art(n, x, y, w, h):
    if n == 1:  # COP31: globe, hills, a rejected draft with a red cross
        d.rectangle([x, y, x + w, y + h], fill=(220, 232, 213))
        d.ellipse([x + w - 78, y + 10, x + w - 38, y + 50], fill=(240, 196, 90))
        d.polygon([(x, y + h), (x + 90, y + 52), (x + 180, y + h)], fill=(150, 178, 130))
        d.polygon([(x + 120, y + h), (x + 220, y + 58), (x + w, y + h)], fill=(120, 155, 105))
        cx, cy, r = x + 78, y + 52, 40
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(126, 166, 200))
        d.ellipse([cx - 26, cy - 30, cx - 2, cy - 6], fill=(110, 160, 105))
        d.ellipse([cx + 2, cy + 8, cx + 28, cy + 30], fill=(110, 160, 105))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(60, 90, 120), width=2)
        d.arc([cx - r, cy - 14, cx + r, cy + 14], 0, 360, fill=(60, 90, 120), width=2)
        # draft document with a red X
        dx, dy = x + w - 92, y + h - 52
        d.rectangle([dx, dy, dx + 56, dy + 40], fill=(250, 248, 240),
                    outline=(120, 110, 95), width=2)
        for i in range(3):
            d.line([(dx + 8, dy + 10 + i * 9), (dx + 48, dy + 10 + i * 9)],
                   fill=(140, 130, 115), width=2)
        d.line([(dx + 4, dy + 2), (dx + 52, dy + 38)], fill=RED, width=5)
        d.line([(dx + 52, dy + 2), (dx + 4, dy + 38)], fill=RED, width=5)
    elif n == 2:  # Hormuz: sea, tanker, missile arcs
        d.rectangle([x, y, x + w, y + h], fill=(216, 228, 238))
        d.ellipse([x + 18, y + 12, x + 58, y + 52], fill=(240, 196, 90))
        for k in range(3):  # waves
            yy = y + 66 + k * 12
            for sx in range(0, w, 44):
                d.arc([x + sx, yy, x + sx + 44, yy + 18], 180, 360,
                      fill=(90, 130, 165), width=3)
        # tanker
        d.polygon([(x + 60, y + 62), (x + 250, y + 62), (x + 238, y + 88),
                   (x + 72, y + 88)], fill=(150, 60, 50))
        for i, c in enumerate([(200, 90, 60), (60, 120, 90), (220, 170, 60)]):
            d.rectangle([x + 88 + i * 48, y + 38, x + 128 + i * 48, y + 62],
                        fill=c, outline=(90, 70, 60), width=2)
        d.rectangle([x + 232, y + 34, x + 252, y + 62], fill=(240, 240, 235))
        d.line([(x + 242, y + 34), (x + 242, y + 20)], fill=INK, width=3)
        # missile arcs
        d.arc([x + 30, y - 6, x + 150, y + 46], 200, 340, fill=RED, width=3)
        d.ellipse([x + 138, y + 8, x + 146, y + 16], fill=RED)
        d.arc([x + 170, y - 2, x + 280, y + 44], 200, 340, fill=RED, width=3)
        d.ellipse([x + 268, y + 10, x + 276, y + 18], fill=RED)
    else:  # summit: three flags over a table
        d.rectangle([x, y, x + w, y + h], fill=(234, 217, 238))
        d.ellipse([x + w - 70, y + 8, x + w - 30, y + 48], fill=(240, 196, 90))
        d.rectangle([x + 30, y + h - 26, x + w - 30, y + h - 12],
                    fill=(120, 85, 60))
        d.rectangle([x + 46, y + h - 40, x + w - 46, y + h - 26],
                    fill=(150, 110, 75))
        flags = [
            (x + 62, [(240, 240, 235), (179, 64, 46), (240, 240, 235),
                      (179, 64, 46), (240, 240, 235)]),   # stripes
            (x + 142, [(179, 64, 46)]),                    # red
            (x + 222, [(240, 240, 235), (46, 94, 140), (179, 64, 46)]),
        ]
        for fx, stripes in flags:
            d.line([(fx, y + 12), (fx, y + h - 40)], fill=INK, width=3)
            fh = 34
            for i, c in enumerate(stripes):
                d.rectangle([fx, y + 14 + i * fh // len(stripes),
                             fx + 52, y + 14 + (i + 1) * fh // len(stripes)],
                            fill=c, outline=(120, 110, 100), width=1)
            if len(stripes) == 1:  # stars on the red flag
                for sx, sy in [(10, 8), (22, 14), (34, 8), (16, 22), (28, 22)]:
                    d.ellipse([fx + sx, y + 14 + sy, fx + sx + 4, y + 18 + sy],
                              fill=(240, 196, 90))

# ---------------------------------------------------------------- heroes
hy = 182
col_w = (CW - 2 * 14) // 3
for i, (num, head, deck, cat, col, city) in enumerate(HEROES):
    x = M + i * (col_w + 14)
    hero_art(num, x, hy, col_w, 96)
    yy = hy + 104
    d.text((x, yy), f"{num}  \u00b7  {cat}  \u00b7  {city}", font=SANS_B(11),
           fill=col)
    yy += 16
    hl = wrap(head, SERIF_B(19), col_w)
    yy = draw_lines(x, yy, hl[:3], SERIF_B(19), INK, 23)
    dl = wrap(deck, SANS(12), col_w)
    draw_lines(x, yy + 2, dl[:2], SANS(12), MUTED, 15)
rule(hy + 210, w=2)

# ---------------------------------------------------------------- features
fy = hy + 224
d.text((M, fy), "TEN MORE STORIES", font=SANS_B(14), fill=INK)
d.text((W - M - text_w("NUMBERED 4\u201313", SANS_B(12)), fy + 1),
       "NUMBERED 4\u201313", font=SANS_B(12), fill=MUTED)
rule(fy + 20, w=1)
fy += 28
fcol_w = (CW - 4 * 9) // 5
for row in range(2):
    for c in range(5):
        num, head, deck, cat, col = FEATURES[row * 5 + c]
        x = M + c * (fcol_w + 9)
        y = fy + row * 78
        d.rectangle([x, y, x + 22, y + 22], fill=col)
        num_s = str(num)
        d.text((x + (22 - text_w(num_s, SANS_B(13))) / 2, y + 3),
               num_s, font=SANS_B(13), fill=(255, 255, 255))
        d.text((x + 28, y + 3), cat, font=SANS_B(10), fill=col)
        hl = wrap(head, SANS_B(12), fcol_w)
        yy = draw_lines(x, y + 24, hl[:2], SANS_B(12), INK, 14)
        dl = wrap(deck, SANS(10), fcol_w)
        draw_lines(x, yy + 2, dl[:2], SANS(10), MUTED, 12)
rule(fy + 162, w=2)

# ---------------------------------------------------------------- map
my = fy + 174
d.text((M, my), "WHERE IT HAPPENED", font=SANS_B(14), fill=INK)
legend = [("CONFLICT", RED), ("DIPLOMACY", BLUE), ("CLIMATE", GREEN),
          ("MARKETS", AMBER), ("SCIENCE", PURPLE), ("DISASTER", BROWN)]
lx = W - M
for name, c in reversed(legend):
    wname = text_w(name, SANS_B(10))
    lx -= wname + 16
    d.ellipse([lx, my + 2, lx + 10, my + 12], fill=c)
    d.text((lx + 13, my + 1), name, font=SANS_B(10), fill=MUTED)
    lx -= 10
rule(my + 20, w=1)
map_y0, map_h = my + 26, 138
d.rectangle([M, map_y0, W - M, map_y0 + map_h], fill=MAP_BG,
            outline=(180, 170, 145), width=1)
land_polys = [
    [(70, 638), (160, 630), (260, 634), (320, 648), (300, 674), (240, 686),
     (170, 684), (100, 674), (60, 656)],
    [(285, 694), (325, 688), (340, 714), (318, 748), (292, 734), (278, 708)],
    [(300, 626), (325, 624), (330, 636), (305, 638)],
    [(500, 636), (545, 631), (572, 642), (552, 658), (515, 654), (495, 646)],
    [(505, 666), (555, 664), (575, 681), (560, 721), (535, 731), (515, 701),
     (500, 681)],
    [(565, 636), (700, 628), (830, 636), (860, 661), (820, 686), (760, 691),
     (680, 686), (600, 676), (565, 658)],
    [(850, 706), (900, 701), (915, 716), (880, 726), (855, 718)],
]
# shift polygons into the map panel (drawn in absolute coords already
# tuned to sit inside the panel: map_y0 == 634 + offset already applied
# by construction, so draw as-is)
for poly in land_polys:
    d.polygon(poly, fill=LAND, outline=(170, 165, 140))
# Mercury glyph for pin 9 (space story)
d.ellipse([918, 634, 942, 658], fill=(190, 175, 160),
          outline=(140, 125, 110), width=1)
d.ellipse([924, 640, 930, 646], fill=(150, 135, 120))
d.ellipse([932, 648, 938, 654], fill=(150, 135, 120))
# small island dots for Indonesia (pins 8 and 11)
d.ellipse([776, 700, 785, 707], fill=LAND, outline=(170, 165, 140))
d.ellipse([800, 710, 809, 717], fill=LAND, outline=(170, 165, 140))
for num, (px, py, col) in sorted(PINS.items()):
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col,
              outline=(255, 255, 255), width=2)
    s = str(num)
    d.text((px - text_w(s, SANS_B(9)) / 2, py - 6), s,
           font=SANS_B(9), fill=(255, 255, 255))
d.text((M + 8, map_y0 + map_h - 16),
       "Pins 1\u201313 mark the hero and feature stories above.  9 = Mercury orbit.",
       font=SANS(10), fill=MUTED)

# ---------------------------------------------------------------- briefs
by = map_y0 + map_h + 12
d.text((M, by), "THE REST OF THE DAY", font=SANS_B(14), fill=INK)
d.text((W - M - text_w("NUMBERED 14\u201345", SANS_B(12)), by + 1),
       "NUMBERED 14\u201345", font=SANS_B(12), fill=MUTED)
rule(by + 20, w=1)
by += 26
f_b = SANS_B(10)
f_t = SANS(10)
col2_w = (CW - 20) // 2
for i, (num, head) in enumerate(BRIEFS):
    col_i = 0 if i < 16 else 1
    row_i = i if i < 16 else i - 16
    x = M + col_i * (col2_w + 20)
    y = by + row_i * 10.5
    ns = f"{num}."
    d.text((x, y), ns, font=f_b, fill=RED)
    d.text((x + text_w("45. ", f_b) + 2, y), head, font=f_t, fill=INK)
fy_end = by + 16 * 10.5 + 4
rule(fy_end, w=2)

# ---------------------------------------------------------------- footer
centered(fy_end + 8,
         "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 The Guardian \u00b7 Euronews \u00b7 Al Jazeera \u00b7 NPR",
         SANS(10), MUTED)
centered(fy_end + 22,
         "Compiled Sunday 22 November 2026 \u2014 all stories checked against the day\u2019s reporting.",
         SANS(10), MUTED)

img.save("entry.png")
print("saved entry.png", img.size, "footer ends at", fy_end + 36)
