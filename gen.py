#!/usr/bin/env python3
"""Render entry.png for make.fun news-image-20261126 (b167, layout V163 ATLAS BANNER).

V163: masthead band; 3 hero columns with art on top; 10 cards 5x2 with a
scene strip on each; full-width world-map strip with 12 numbered pins;
3-column ALSO list (37 items); 2-line DATE CHECK footer.
All copy is English. 50 stories total: 3 heroes + 10 cards + 37 ALSO.
"""
import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu"
F_SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
F_SANS = os.path.join(FD, "DejaVuSans.ttf")
F_SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")

# ---- palette ----
PAPER = (247, 243, 234)
INK = (20, 32, 43)
NAVY = (15, 37, 64)
NAVY2 = (27, 58, 95)
RED = (179, 38, 30)
RED_D = (140, 28, 22)
GOLD = (201, 162, 39)
CREAM = (255, 243, 214)
CARD_BG = (255, 255, 255)
CARD_LINE = (216, 210, 196)
MUTED = (90, 100, 112)
OCEAN = (207, 227, 238)
LAND = (222, 230, 198)
LAND_LINE = (150, 165, 130)
PIN_RED = (178, 34, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

_cache = {}


def F(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(draw, text, font, maxw):
    """Greedy word wrap; returns list of lines that fit maxw."""
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---- overlap / bounds bookkeeping (asserts run at the end) ----
TEXTBOXES = []  # (bbox, parent, label, on_art)
ARTRECTS = []   # (rect, label)


def draw_text(draw, xy, text, font, fill, parent, label, on_art=False, anchor="la"):
    bbox = draw.textbbox(xy, text, font=font, anchor=anchor)
    TEXTBOXES.append((bbox, parent, label, on_art))
    draw.text(xy, text, font=font, fill=fill, anchor=anchor)
    return bbox


def draw_para(draw, x, y, lines, font, fill, parent, label, lh, on_art=False):
    boxes = []
    for ln in lines:
        boxes.append(draw_text(draw, (x, y), ln, font, fill, parent,
                               label, on_art=on_art))
        y += lh
    return boxes, y

# ============================ DATA ============================
# Heroes: (kicker, headline, deck, why, bignum, art_key)
HEROES = [
    ("NEW YORK  ·  CULTURE & WEATHER",
     "Macy's 100th Parade Postponed by Storm",
     "Thanksgiving parade delayed for the first time ever by weather; "
     "60 mph gusts ground the giant balloons.",
     "WHY IT MATTERS: America's biggest holiday ritual, in its 100th "
     "year, yields to a storm — a first ever.",
     "100TH", "parade"),
    ("STRAIT OF HORMUZ  ·  ENERGY & WAR",
     "Iran Claims 2 Tankers Hit by Mines",
     "IRGC says two tankers, one carrying 2M barrels, hit sea mines "
     "in the Strait. The claim is unverified.",
     "WHY IT MATTERS: The world's busiest oil chokepoint is now a "
     "minefield claim — Brent crude jumped as war widens.",
     "2M", "tanker"),
    ("GLOBAL MARKETS  ·  TRADE",
     "Markets Rebound as Tariffs Look Softer",
     "Stocks in Europe and Asia rally as Trump's tariff salvo lands "
     "milder than feared; duties will not stack.",
     "WHY IT MATTERS: A 14-partner plan led by 20% on China was priced "
     "as a shock — markets now call it modest.",
     "+1.6%", "market"),
]

# Cards: (region, headline, deck, badge, art_key, scene_bg)
CARDS = [
    ("GAZA", "Israeli strike kills Hamas education chief",
     "Khaled Abu Nada and wife die in Deir al-Balah; 9 killed. [C]",
     "9", "gaza", (122, 74, 62)),
    ("KYIV", "Russian missile hits Kyiv mall",
     "Ballistic strike wounds 7; 113 drones overnight. [C]",
     "7", "kyiv", (70, 70, 78)),
    ("BOGOR", "Flooded gold mine: 13 dead, 13 missing",
     "Illegal mine floods ~100 m underground after heavy rain. [C]",
     "13", "bogor", (46, 92, 74)),
    ("JERUSALEM", "Judge urges dropping Netanyahu bribery charge",
     "Court urges prosecutors to drop Case 4000, sole bribery count. [R]",
     "4000", "court", (94, 82, 52)),
    ("PYONGYANG", "Kim tours nuclear plant, urges tactical nukes",
     "Kim presses wider use of tactical nuclear arms. [R]",
     "1", "nuke", (88, 40, 48)),
    ("SPACE", "FCC clears SpaceX's 1M orbital data satellites",
     "FCC nod, given 25 Nov, first for data centres in orbit. [C]",
     "1M", "space", (38, 52, 96)),
    ("LONDON", "UK net migration falls to 77,000",
     "Lowest since 1997 outside the pandemic, ONS figures show. [C]",
     "77K", "uk", (52, 84, 120)),
    ("MOSCOW", "Russia approves record post-Soviet arms budget",
     "Military spending hits a post-Soviet high as war grinds on. [C]",
     "08", "budget", (96, 96, 96)),
    ("BANGKOK", "Oil depot blast injures 7 in Bangkok",
     "Blast at Bangkok oil depot triggers evacuation warnings. [C]",
     "7", "blast", (150, 96, 32)),
    ("GERMANY", "2 held in Germany over synagogue plot",
     "Iraqi suspects held in Cologne, Heidelberg; raids carried out. [C]",
     "2", "arrest", (58, 84, 88)),
]

# ALSO: exactly 37 distinct stories, one line each.
ALSO = [
    "Eisenkot clinches first Israel coalition deal [R]",
    "Merz warns Russia's aims go beyond Ukraine [R]",
    "UK air bases on alert over drone threat [R]",
    "Norse Atlantic halts all flights, warns of collapse [C]",
    "Poundland enters administration; 11,000 jobs at risk [C]",
    "Malaysia sues Google for $146m over harmful content [C]",
    "Kenya court halts US-backed Ebola facility [C]",
    "Belarus offers to fly Zelensky to Moscow; he refuses [R]",
    "Kushner calls Putin 'grandmaster of politics' [R]",
    "Estonia decides to close its border [C]",
    "Copernicus: longest stretch above 2°C confirmed [C]",
    "Nvidia halts AI server shipments to 4 nations [R]",
    "US Bitcoin ETFs: record $4.94bn Nov outflows [C]",
    "Philadelphia Thanksgiving parade also cancelled [C]",
    "Brent $93.8 (+0.9%); WTI $83.32 [C]",
    "Nvidia shares -3.91% to $149.30 [C]",
    "Gold $3,572/oz, down 0.2% on Thursday [C]",
    "S&P, Nasdaq futures +0.5% as Wall St shuts [C]",
    "Ukraine drones damage 5 jets at Savasleyka base [R]",
    "Kharkiv couple, 37 and 38, killed in flat strike [C]",
    "18 wounded in Kryvyi Rih strike [C]",
    "UN rights chief Turk warns of atrocity risk in Gaza [R]",
    "Saudi defences down 2 missiles headed for Riyadh [R]",
    "Duran Duran guitarist Andy Taylor dies aged 65 [C]",
    "UKMTO: blast near tanker 50 nm west of Dubai [C]",
    "UKMTO: tanker hit off Khasab, 25 Nov [CL]",
    "OPEC+ to meet 29 Nov on 2027 output [R]",
    "Bank of Korea raises rate to 3.25% [C]",
    "Macy's balloons inflated, then deflated again [C]",
    "NBC airs 2025 parade Thu; live parade Sat 08:30 ET [C]",
    "Tariffs will not stack on July duties [R]",
    "Russia claims drone-site strikes in Kyiv [CL]",
    "Cargo ship near Odesa claimed hit [CL]",
    "Subkhankulovo pump station ablaze in Russia [R]",
    "Dollar flat at 103.71 [C]",
    "Nvidia $2.3tn below October peak [C]",
    "Bangkok depot fire out in ~30 min; output shut [C]",
]

# DATE CHECK: exactly 7 exclusions, rendered as 2 lines (4 + 3).
# Verbatim list (coordinator, 27 Nov): these 7 strings, no paraphrase.
DATECHECK = [
    "COP31 failed 22 Nov",
    "Shenzhou-24 launched 25 Nov",
    "Cairo tanker blast, 31 dead, 25 Nov",
    "Cartagena hostages freed 25 Nov",
    "Australia-Solomon pact 25 Nov",
    "UK energy prices +26% announced 25 Nov",
    "Huawei convicted 24 Nov",
]

EXPECTED_DATECHECK = [
    "COP31 failed 22 Nov",
    "Shenzhou-24 launched 25 Nov",
    "Cairo tanker blast, 31 dead, 25 Nov",
    "Cartagena hostages freed 25 Nov",
    "Australia-Solomon pact 25 Nov",
    "UK energy prices +26% announced 25 Nov",
    "Huawei convicted 24 Nov",
]

# Map pins: (number, name, lon, lat). Longitudes for Indonesia are POSITIVE.
PINS = [
    ("01", "NEW YORK", -74.00, 40.71),
    ("02", "LONDON", -0.12, 51.50),
    ("03", "COLOGNE", 6.96, 50.94),
    ("04", "KYIV", 30.52, 50.45),
    ("05", "MOSCOW", 37.62, 55.76),
    ("06", "GAZA", 34.45, 31.50),
    ("07", "KHASAB", 56.25, 26.18),
    ("08", "RIYADH", 46.68, 24.71),
    ("09", "NAIROBI", 36.82, -1.29),
    ("10", "BANGKOK", 100.50, 13.75),
    ("11", "BOGOR", 106.80, -6.60),
    ("12", "PYONGYANG", 125.75, 39.03),
]

# ---- coarse continent outlines (lon, lat) for the stylised world map ----
POLYS = [
    # North America
    [(-168, 66), (-160, 58), (-155, 58), (-150, 60), (-145, 60), (-140, 60),
     (-135, 58), (-130, 54), (-125, 49), (-124, 42), (-120, 34), (-114, 29),
     (-110, 24), (-105, 20), (-100, 18), (-95, 16), (-90, 14), (-86, 12),
     (-83, 9), (-80, 8), (-77, 8), (-79, 10), (-82, 10), (-84, 13), (-87, 16),
     (-88, 18), (-90, 19), (-93, 19), (-96, 19), (-97, 24), (-97, 26),
     (-94, 29), (-90, 30), (-85, 30), (-82, 28), (-81, 25), (-80, 27),
     (-80, 32), (-76, 35), (-74, 39), (-72, 41), (-70, 42), (-68, 44),
     (-65, 44), (-60, 46), (-55, 47), (-59, 50), (-64, 52), (-65, 58),
     (-68, 58), (-72, 62), (-76, 62), (-80, 66), (-85, 66), (-90, 68),
     (-95, 69), (-100, 68), (-110, 68), (-120, 69), (-130, 70), (-140, 70),
     (-150, 71), (-160, 71), (-165, 68), (-168, 66)],
    # South America
    [(-77, 8), (-75, 10), (-72, 12), (-68, 11), (-64, 10), (-60, 8), (-55, 6),
     (-52, 4), (-50, 0), (-48, -5), (-45, -8), (-40, -10), (-37, -13),
     (-39, -17), (-41, -22), (-45, -24), (-48, -27), (-50, -30), (-53, -33),
     (-55, -35), (-58, -38), (-62, -40), (-65, -43), (-67, -46), (-68, -50),
     (-70, -53), (-72, -54), (-73, -50), (-73, -45), (-73, -40), (-72, -35),
     (-71, -30), (-70, -25), (-70, -20), (-72, -18), (-75, -15), (-77, -12),
     (-79, -8), (-80, -5), (-81, -3), (-80, 0), (-78, 3), (-77, 6), (-77, 8)],
    # Greenland
    [(-45, 60), (-40, 64), (-32, 68), (-25, 70), (-20, 72), (-25, 74),
     (-35, 76), (-50, 76), (-58, 74), (-55, 70), (-52, 66), (-48, 62),
     (-45, 60)],
    # Africa
    [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 12),
     (-12, 8), (-8, 5), (-4, 5), (0, 6), (6, 4), (9, 4), (9, 0), (12, -5),
     (13, -10), (12, -15), (14, -20), (16, -25), (18, -30), (20, -35),
     (25, -34), (28, -33), (32, -29), (35, -25), (36, -20), (38, -15),
     (40, -10), (41, -5), (42, -1), (44, 2), (46, 5), (48, 10), (50, 11),
     (48, 11), (45, 11), (43, 12), (41, 13), (39, 15), (38, 18), (37, 20),
     (36, 22), (35, 25), (34, 28), (32, 31), (30, 31), (25, 32), (20, 32),
     (15, 32), (11, 33), (10, 34), (10, 37), (8, 37), (5, 37), (0, 36),
     (-2, 35), (-6, 35)],
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (50, -20), (48, -24), (45, -25),
     (44, -22), (43, -18), (44, -16)],
    # Europe + northern Asia (one big landmass)
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 50), (2, 51),
     (4, 52), (7, 54), (8, 57), (11, 58), (18, 56), (21, 57), (24, 59),
     (28, 60), (30, 62), (32, 66), (35, 68), (40, 68), (45, 68), (50, 69),
     (55, 69), (60, 69), (65, 69), (68, 68), (70, 66), (68, 64), (60, 60),
     (55, 58), (50, 55), (45, 52), (40, 50), (38, 47), (35, 45), (33, 44),
     (30, 45), (28, 44), (24, 42), (22, 40), (20, 40), (18, 40), (16, 40),
     (14, 42), (12, 44), (10, 44), (8, 44), (6, 43), (3, 43), (0, 40),
     (-2, 37), (-6, 36), (-10, 36)],
    # East / South Asia coast (Siberia down to SE Asia, via China coast)
    [(30, 62), (40, 68), (55, 69), (70, 72), (90, 75), (110, 74), (130, 72),
     (150, 70), (162, 60), (158, 52), (142, 42), (135, 35), (127, 35),
     (126, 39), (122, 38), (120, 32), (122, 28), (118, 25), (110, 21),
     (108, 18), (105, 10), (103, 8), (100, 7), (98, 10), (97, 15), (94, 17),
     (92, 21), (90, 22), (88, 22), (86, 20), (82, 17), (80, 13), (77, 8),
     (75, 12), (73, 16), (70, 20), (66, 25), (62, 25), (58, 26), (57, 27),
     (56, 27), (54, 26), (52, 25), (50, 26), (49, 29), (48, 30), (46, 29),
     (44, 29), (42, 28), (40, 30), (39, 32), (38, 35), (36, 36), (35, 38),
     (33, 40), (30, 42), (28, 44), (27, 41), (26, 40), (24, 40), (22, 40),
     (20, 40), (18, 40), (16, 40), (14, 42), (12, 44), (10, 44), (8, 44),
     (6, 43), (3, 43), (0, 40), (-2, 37), (-6, 36), (-9, 37), (-9, 43),
     (-2, 46), (-4, 48), (0, 50), (2, 52), (5, 53), (8, 57), (11, 58),
     (18, 56), (21, 57), (24, 59), (28, 60), (30, 62)],
    # Arabian peninsula (with Levant coast so Gaza sits on land)
    [(34, 32), (35, 29), (36, 29), (37, 25), (39, 20), (41, 15), (43, 12.7),
     (45, 13), (48, 14), (52, 15), (55, 17), (58, 20), (59, 23), (58, 25),
     (56, 27), (54, 26), (52, 25), (50, 26), (48, 26), (43, 27), (39, 28),
     (35, 29), (34, 32)],
    # India
    [(66, 25), (68, 22), (70, 20), (72, 18), (74, 14), (76, 9), (78, 8),
     (80, 9), (80, 13), (82, 16), (85, 19), (88, 22), (90, 22), (92, 21),
     (94, 17), (96, 16), (97, 16), (95, 20), (93, 24), (90, 26), (88, 26),
     (86, 26), (84, 24), (82, 22), (80, 20), (78, 18), (76, 20), (74, 24),
     (72, 25), (70, 26), (68, 25), (66, 25)],
    # SE Asia mainland
    [(97, 16), (98, 12), (100, 7), (101, 6), (103, 2), (104, 2), (105, 8),
     (107, 10), (109, 13), (109, 15), (106, 18), (105, 20), (102, 22),
     (100, 22), (98, 20), (97, 16)],
    # Korea
    [(126, 34.5), (127.5, 35), (129, 35.5), (129.5, 38), (128, 39.5),
     (126.5, 39.8), (124.5, 39.8), (124, 38), (125, 36), (126, 34.5)],
    # Japan
    [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
     (141, 39), (141, 42), (142, 44), (143, 44), (141, 42), (140, 38),
     (139, 37), (137, 36), (135, 34), (133, 34), (131, 33), (130, 31)],
    # UK
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
     (-1, 50), (-3, 50), (-5, 50)],
    # Sumatra
    [(95, 5), (96, 4), (98, 2), (100, 0), (102, -2), (104, -3), (106, -5),
     (105, -5.5), (103, -4), (101, -1), (99, 2), (97, 5), (95, 5)],
    # Java (Bogor pin must sit on this island)
    [(105, -6), (107, -6.5), (109, -6.8), (111, -6.8), (113, -7), (114, -7.5),
     (114, -8.5), (112, -7.8), (110, -7.8), (108, -7.7), (106, -7.7),
     (105, -6.8), (105, -6)],
    # Borneo
    [(109, 1), (110, 2), (112, 4), (114, 5), (116, 6), (118, 4), (117, 1),
     (116, -1), (114, -3), (112, -3), (110, -2), (109, 0), (109, 1)],
    # New Guinea
    [(131, -1), (133, -2), (136, -2), (138, -3), (140, -4), (141, -6),
     (140, -8), (137, -8), (134, -7), (132, -5), (131, -3), (131, -1)],
    # Australia
    [(113, -22), (114, -30), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
     (141, -13), (140, -17), (136, -15), (135, -12), (132, -11), (130, -13),
     (127, -14), (124, -17), (122, -18), (120, -20), (117, -20), (114, -22),
     (113, -22)],
    # New Zealand
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38), (175, -40),
     (173, -42), (170, -44), (168, -46), (167, -45)],
]

# Map geometry: equirectangular lon -130..150, lat -58..78.
MAP_X0, MAP_Y0, MAP_X1, MAP_Y1 = 20, 548, 1004, 696
MAP_LON0, MAP_LON1, MAP_LAT0, MAP_LAT1 = -130.0, 150.0, -58.0, 78.0


def proj(lon, lat):
    x = MAP_X0 + (lon - MAP_LON0) / (MAP_LON1 - MAP_LON0) * (MAP_X1 - MAP_X0)
    y = MAP_Y0 + (MAP_LAT1 - lat) / (MAP_LAT1 - MAP_LAT0) * (MAP_Y1 - MAP_Y0)
    return x, y


def draw_map(draw, mask_draw):
    """Draw ocean + land polygons on a LOCAL map-sized layer (so nothing
    can bleed outside the map rectangle). Local origin = map top-left."""
    mw, mh = MAP_X1 - MAP_X0, MAP_Y1 - MAP_Y0
    draw.rectangle([0, 0, mw, mh], fill=OCEAN)
    for poly in POLYS:
        pts = [(proj(lon, lat)[0] - MAP_X0, proj(lon, lat)[1] - MAP_Y0)
               for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_LINE)
        mask_draw.polygon(pts, fill=255)
    # graticule
    for lon in range(-120, 151, 30):
        x, _ = proj(lon, 0)
        draw.line([(x - MAP_X0, 0), (x - MAP_X0, mh)],
                  fill=(255, 255, 255, 90), width=1)
    for lat in (-40, -20, 0, 20, 40, 60):
        _, y = proj(0, lat)
        draw.line([(0, y - MAP_Y0), (mw, y - MAP_Y0)],
                  fill=(255, 255, 255, 90), width=1)
    draw.rectangle([0, 0, mw - 1, mh - 1], outline=MUTED, width=1)

# ============================ ART ============================
def hero_art(draw, rect, key):
    """Geometric scene inside rect; returns nothing. Badge text is drawn
    by the caller (flagged on_art so the overlap check skips it)."""
    x0, y0, x1, y1 = rect
    ARTRECTS.append((rect, "hero-" + key))
    w, h = x1 - x0, y1 - y0
    if key == "parade":
        draw.rectangle(rect, fill=(58, 98, 150))
        # storm clouds
        for cx, cy, r in [(x0 + 60, y0 + 18, 26), (x0 + 150, y0 + 12, 30),
                          (x0 + 250, y0 + 20, 24)]:
            draw.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
                         fill=(200, 205, 212))
        # skyline
        for bx, bw, bh in [(0, 34, 34), (40, 26, 48), (72, 30, 30),
                           (108, 28, 52), (142, 34, 36), (182, 26, 46),
                           (214, 30, 32), (250, 28, 44), (284, 34, 38)]:
            draw.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1],
                           fill=(32, 48, 70))
        # balloons: big ellipses above the skyline
        draw.ellipse([x0 + 55, y0 + 30, x0 + 125, y0 + 72], fill=(179, 38, 30))
        draw.ellipse([x0 + 150, y0 + 26, x0 + 205, y0 + 62], fill=(232, 190, 40))
        draw.ellipse([x0 + 225, y0 + 34, x0 + 275, y0 + 66], fill=(240, 240, 235))
        draw.line([(x0 + 90, y0 + 72), (x0 + 90, y1 - 34)], fill=(240, 240, 235),
                  width=2)
        draw.line([(x0 + 178, y0 + 62), (x0 + 178, y1 - 48)], fill=(240, 240, 235),
                  width=2)
    elif key == "tanker":
        draw.rectangle(rect, fill=(24, 58, 86))
        # sun / haze
        draw.ellipse([x0 + w - 70, y0 + 8, x0 + w - 26, y0 + 52], fill=(232, 190, 40))
        # sea
        draw.rectangle([x0, y0 + h - 34, x1, y1], fill=(46, 110, 150))
        for wy in (y0 + h - 26, y0 + h - 14):
            for wx in range(x0 + 6, x1 - 10, 26):
                draw.arc([wx, wy, wx + 22, wy + 12], 0, 180, fill=(255, 255, 255),
                         width=2)
        # tanker hull + deck
        draw.rectangle([x0 + 40, y0 + h - 62, x0 + w - 60, y0 + h - 34],
                       fill=(30, 30, 34))
        draw.rectangle([x0 + w - 108, y0 + h - 84, x0 + w - 60, y0 + h - 62],
                       fill=(200, 205, 212))
        draw.rectangle([x0 + 52, y0 + h - 76, x0 + 96, y0 + h - 62],
                       fill=(179, 38, 30))
        # flames + smoke
        draw.polygon([(x0 + 120, y0 + h - 62), (x0 + 132, y0 + h - 86),
                      (x0 + 146, y0 + h - 62)], fill=(240, 120, 20))
        draw.polygon([(x0 + 150, y0 + h - 62), (x0 + 160, y0 + h - 80),
                      (x0 + 172, y0 + h - 62)], fill=(240, 180, 40))
        for cx, cy, r in [(x0 + 130, y0 + 22, 12), (x0 + 148, y0 + 14, 15),
                          (x0 + 168, y0 + 24, 11)]:
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 90, 96))
        # mines (spiked circles) in the water
        for mx, my in [(x0 + 26, y0 + h - 18), (x0 + w - 30, y0 + h - 16)]:
            draw.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(20, 20, 24))
            draw.line([(mx - 11, my), (mx + 11, my)], fill=(20, 20, 24), width=2)
            draw.line([(mx, my - 11), (mx, my + 11)], fill=(20, 20, 24), width=2)
    else:  # market
        draw.rectangle(rect, fill=(28, 74, 54))
        # rising bars
        bars = [(18, 34), (52, 44), (86, 40), (120, 56), (154, 62),
                (188, 72), (222, 84), (256, 92)]
        for bx, bh in bars:
            draw.rectangle([x0 + bx, y1 - bh, x0 + bx + 24, y1 - 8],
                           fill=(232, 190, 40))
        # trend arrow
        pts = [(x0 + 18, y1 - 40), (x0 + 64, y1 - 50), (x0 + 98, y1 - 46),
               (x0 + 132, y1 - 62), (x0 + 166, y1 - 68), (x0 + 200, y1 - 78),
               (x0 + 234, y1 - 90), (x0 + 280, y1 - 98)]
        draw.line(pts, fill=(255, 255, 255), width=4, joint="curve")
        draw.polygon([(x0 + 268, y1 - 108), (x0 + 292, y1 - 100),
                      (x0 + 272, y1 - 88)], fill=(255, 255, 255))
        # containers
        for cx, cy, col in [(x0 + 20, y0 + 12, (179, 38, 30)),
                            (x0 + 52, y0 + 12, (46, 110, 150)),
                            (x0 + 36, y0 + 26, (232, 190, 40))]:
            draw.rectangle([cx, cy, cx + 28, cy + 12], fill=col,
                           outline=(255, 255, 255))


def card_scene(draw, rect, key, bg):
    x0, y0, x1, y1 = rect
    ARTRECTS.append((rect, "card-" + key))
    draw.rectangle(rect, fill=bg)
    cx, cy = x0 + 22, y0 + 14
    if key == "gaza":
        for bx, bw, bh in [(8, 12, 16), (24, 10, 20), (38, 12, 14)]:
            draw.rectangle([x0 + bx, y1 - bh - 2, x0 + bx + bw, y1 - 2],
                           fill=(230, 220, 200))
        draw.polygon([(x0 + 26, y0 + 6), (x0 + 32, y0 + 14),
                      (x0 + 20, y0 + 14)], fill=(240, 180, 40))
    elif key == "kyiv":
        draw.polygon([(cx, cy - 10), (cx + 3, cy - 3), (cx + 10, cy - 2),
                      (cx + 4, cy + 3), (cx + 6, cy + 10), (cx, cy + 6),
                      (cx - 6, cy + 10), (cx - 4, cy + 3), (cx - 10, cy - 2),
                      (cx - 3, cy - 3)], fill=(240, 180, 40))
        draw.rectangle([x0 + 44, y1 - 12, x1 - 40, y1 - 4], fill=(60, 60, 68))
    elif key == "bogor":
        draw.rectangle([x0 + 10, y0 + 4, x0 + 34, y1 - 4], fill=(30, 30, 34))
        draw.rectangle([x0 + 14, y0 + 8, x0 + 30, y1 - 8], fill=(46, 110, 150))
    elif key == "court":
        draw.rectangle([x0 + 12, y0 + 8, x0 + 34, y0 + 12], fill=(232, 190, 40))
        draw.rectangle([x0 + 21, y0 + 12, x0 + 25, y0 + 20], fill=(232, 190, 40))
        draw.rectangle([x0 + 14, y0 + 20, x0 + 32, y0 + 23], fill=(232, 190, 40))
    elif key == "nuke":
        draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=(240, 240, 235),
                     width=2)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(240, 180, 40))
    elif key == "space":
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(240, 240, 235))
        draw.rectangle([cx - 12, cy - 2, cx - 5, cy + 2], fill=(200, 205, 212))
        draw.rectangle([cx + 5, cy - 2, cx + 12, cy + 2], fill=(200, 205, 212))
        for sx, sy in [(x0 + 48, y0 + 6), (x0 + 58, y0 + 18), (x0 + 44, y0 + 20)]:
            draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    elif key == "uk":
        draw.rectangle([x0 + 8, y0 + 6, x0 + 36, y0 + 22], fill=(179, 38, 30))
        draw.line([(x0 + 8, y0 + 14), (x0 + 36, y0 + 14)], fill=(255, 255, 255),
                  width=3)
        draw.line([(x0 + 22, y0 + 6), (x0 + 22, y0 + 22)], fill=(255, 255, 255),
                  width=3)
    elif key == "budget":
        for bx, bh in [(8, 8), (18, 14), (28, 20)]:
            draw.rectangle([x0 + bx, y1 - 4 - bh, x0 + bx + 7, y1 - 4],
                           fill=(232, 190, 40))
    elif key == "blast":
        draw.polygon([(cx, cy - 11), (cx + 4, cy - 4), (cx + 11, cy - 6),
                      (cx + 6, cy), (cx + 10, cy + 7), (cx + 2, cy + 6),
                      (cx, cy + 12), (cx - 3, cy + 5), (cx - 11, cy + 6),
                      (cx - 6, cy), (cx - 10, cy - 6), (cx - 3, cy - 4)],
                     fill=(240, 120, 20))
    else:  # arrest
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=(255, 255, 255),
                     width=2)
        draw.line([(cx - 4, cy - 4), (cx + 4, cy + 4)], fill=(255, 255, 255),
                  width=2)
        draw.line([(cx + 4, cy - 4), (cx - 4, cy + 4)], fill=(255, 255, 255),
                  width=2)

# ============================ RENDER ============================
def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    mask = Image.new("L", (W, H), 0)
    mask_draw = ImageDraw.Draw(mask)

    # ---- masthead ----
    mh = (14, 10, 1010, 82)
    draw.rectangle(mh, fill=NAVY)
    draw.rectangle([14, 80, 1010, 82], fill=GOLD)
    draw_text(draw, (26, 20), "THE WORLD IN ONE DAY", F(F_SERIF_B, 30),
              WHITE, mh, "masthead-title")
    draw_text(draw, (26, 56), "50 STORIES  ·  10 REGIONS  ·  MAKE.FUN",
              F(F_SANS_B, 10), (200, 205, 212), mh, "masthead-sub")
    draw_text(draw, (998, 20), "THURSDAY 26 NOVEMBER 2026", F(F_SANS_B, 19),
              WHITE, mh, "masthead-date", anchor="ra")
    draw_text(draw, (998, 50), "NEWS-IMAGE-20261126", F(F_SANS, 10),
              (200, 205, 212), mh, "masthead-slug", anchor="ra")

    # ---- heroes: 3 columns ----
    hx = [14, 349, 684]
    hw = [327, 327, 326]
    hy0, hy1 = 90, 330
    for (kicker, head, deck, why, big, key), x0, w in zip(HEROES, hx, hw):
        box = (x0, hy0, x0 + w, hy1)
        draw.rectangle(box, fill=CARD_BG, outline=CARD_LINE, width=1)
        art = (x0 + 1, hy0 + 1, x0 + w - 1, hy0 + 105)
        hero_art(draw, art, key)
        # big-number badge, bottom-right of the art (on art by design)
        bf = F(F_SANS_B, 17)
        bw = draw.textlength(big, font=bf) + 16
        bx0, by0 = art[2] - bw - 6, art[3] - 30
        draw.rectangle([bx0, by0, bx0 + bw, by0 + 24], fill=RED)
        draw_text(draw, (bx0 + 8, by0 + 3), big, bf, WHITE, box,
                  "hero-badge-" + key, on_art=True)
        y = hy0 + 112
        draw_text(draw, (x0 + 10, y), kicker, F(F_SANS_B, 9), RED, box,
                  "hero-kicker-" + key)
        y += 16
        hl = wrap(draw, head, F(F_SANS_B, 16), w - 20)
        _, y = draw_para(draw, x0 + 10, y, hl, F(F_SANS_B, 16), INK, box,
                         "hero-head-" + key, 19)
        y += 4
        dl = wrap(draw, deck, F(F_SANS, 11), w - 20)
        _, y = draw_para(draw, x0 + 10, y, dl, F(F_SANS, 11), INK, box,
                         "hero-deck-" + key, 14)
        y += 5
        wl = wrap(draw, why, F(F_SANS, 10), w - 20)
        draw_para(draw, x0 + 10, y, wl, F(F_SANS, 10), MUTED, box,
                  "hero-why-" + key, 13)

    # ---- cards: 5 cols x 2 rows ----
    cw = [193, 193, 193, 193, 192]
    cx = [14, 215, 416, 617, 818]
    cy0 = [338, 431]
    ch = 89
    for i, (region, head, deck, badge, key, bg) in enumerate(CARDS):
        r, c = divmod(i, 5)
        x0, y0 = cx[c], cy0[r]
        box = (x0, y0, x0 + cw[c], y0 + ch)
        draw.rectangle(box, fill=CARD_BG, outline=CARD_LINE, width=1)
        scene = (x0 + 1, y0 + 1, x0 + cw[c] - 1, y0 + 29)
        card_scene(draw, scene, key, bg)
        draw_text(draw, (x0 + 46, y0 + 9), region, F(F_SANS_B, 10), WHITE,
                  box, "card-region-" + key, on_art=True)
        # number badge: white circle at the right end of the scene
        bx, by = x0 + cw[c] - 20, y0 + 15
        draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=WHITE,
                     outline=INK, width=1)
        bf = F(F_SANS_B, 10 if len(badge) <= 2 else 8)
        tw = draw.textlength(badge, font=bf)
        draw_text(draw, (bx - tw / 2, by - 6 if len(badge) <= 2 else by - 5),
                  badge, bf, INK, box, "card-badge-" + key, on_art=True)
        y = y0 + 33
        hl = wrap(draw, head, F(F_SANS_B, 11), cw[c] - 14)
        _, y = draw_para(draw, x0 + 7, y, hl, F(F_SANS_B, 11), INK, box,
                         "card-head-" + key, 13)
        y += 1
        dl = wrap(draw, deck, F(F_SANS, 10), cw[c] - 14)
        draw_para(draw, x0 + 7, y, dl, F(F_SANS, 10), INK, box,
                  "card-deck-" + key, 12)

    # ---- map strip (rendered on its own layer, clipped to the rect) ----
    mp = (14, 524, 1010, 716)
    draw.rectangle(mp, fill=CARD_BG, outline=CARD_LINE, width=1)
    draw_text(draw, (24, 530), "WHERE IT HAPPENED — 12 PINS",
              F(F_SANS_B, 11), NAVY, mp, "map-title")
    mw, mh = MAP_X1 - MAP_X0, MAP_Y1 - MAP_Y0
    map_img = Image.new("RGB", (mw, mh), OCEAN)
    map_mask = Image.new("L", (mw, mh), 0)
    draw_map(ImageDraw.Draw(map_img), ImageDraw.Draw(map_mask))
    img.paste(map_img, (MAP_X0, MAP_Y0))
    mask.paste(map_mask, (MAP_X0, MAP_Y0))
    pin_r = 8
    pin_xy = {}
    for num, name, lon, lat in PINS:
        px, py = proj(lon, lat)
        pin_xy[num] = (px, py)
        draw.ellipse([px - pin_r, py - pin_r, px + pin_r, py + pin_r],
                     fill=PIN_RED, outline=WHITE, width=2)
        nf = F(F_SANS_B, 8)
        tw = draw.textlength(num, font=nf)
        draw_text(draw, (px - tw / 2, py - 5), num, nf, WHITE, mp,
                  "pin-" + num, on_art=True)
    legend = "  ·  ".join("%s %s" % (n, name) for n, name, _, _ in PINS)
    draw_text(draw, (512, 700), legend, F(F_SANS, 9), MUTED, mp,
              "map-legend", anchor="ma")

    # ---- ALSO: 3 columns ----
    ap = (14, 724, 1010, 962)
    draw.rectangle(ap, fill=CARD_BG, outline=CARD_LINE, width=1)
    draw_text(draw, (24, 730), "ALSO ON 26 NOVEMBER — 37 MORE STORIES",
              F(F_SANS_B, 12), NAVY, ap, "also-title")
    draw.line([(24, 750), (1000, 750)], fill=CARD_LINE, width=1)
    cols = [ALSO[0:13], ALSO[13:25], ALSO[25:37]]
    colx = [24, 356, 688]
    colw = 310
    afont = F(F_SANS, 10)
    for col, x0 in zip(cols, colx):
        y = 758
        for item in col:
            draw_text(draw, (x0, y), "•  " + item, afont, INK, ap,
                      "also-item")
            y += 14

    # ---- DATE CHECK footer: exactly 7 exclusions, 2 lines ----
    dp = (14, 970, 1010, 1014)
    draw.rectangle(dp, fill=CREAM, outline=GOLD, width=1)
    dfont = F(F_SANS, 10)
    dbfont = F(F_SANS_B, 10)
    line1 = "DATE CHECK — NOT 26 NOV:  " + "  ·  ".join(DATECHECK[:4])
    line2 = "  ·  ".join(DATECHECK[4:])
    draw_text(draw, (24, 976), line1, dfont, INK, dp, "datecheck-1")
    draw_text(draw, (24, 993), line2, dfont, INK, dp, "datecheck-2")

    # ============================ ASSERTS ============================
    assert len(ALSO) == 37, "ALSO must be 37, got %d" % len(ALSO)
    assert len(DATECHECK) == 7, "DATE CHECK must be 7, got %d" % len(DATECHECK)
    assert DATECHECK == EXPECTED_DATECHECK, \
        "DATE CHECK list mismatch: %r" % (DATECHECK,)
    # hard defects from the coordinator zoom-check (b167 revision):
    # hero-2 deck must not mix the IRGC mine claim with the UKMTO
    # Khasab incident (that one is its own ALSO item).
    assert "near Khasab" not in HEROES[1][2], \
        "hero-2 deck still contains 'near Khasab'"
    assert "Ras Tanura" not in "  ".join(DATECHECK), \
        "DATE CHECK must not contain Ras Tanura"
    assert "tariffs announced" not in "  ".join(DATECHECK).lower(), \
        "DATE CHECK must not contain tariffs announced"
    # no duplicate story: Bogor appears exactly once, as a card, never ALSO.
    assert sum(1 for c in CARDS if c[0] == "BOGOR") == 1, "Bogor card != 1"
    assert not any("Bogor" in item for item in ALSO), \
        "Bogor duplicated in ALSO"
    # every card deck carries a literal [C]/[R]/[CL] tag
    for region, head, deck, badge, key, bg in CARDS:
        assert deck.rsplit("[", 1)[1].rstrip("]") in ("C", "R", "CL"), \
            "card %s deck missing tag: %s" % (key, deck)
    assert len(PINS) == 12, "pins must be 12, got %d" % len(PINS)
    assert len(HEROES) + len(CARDS) + len(ALSO) == 50, "total stories != 50"

    # all text inside its parent box, margin >= 2px
    for bbox, parent, label, on_art in TEXTBOXES:
        assert bbox[0] >= parent[0] + 2 - 0.5, "%s left %s" % (label, bbox)
        assert bbox[1] >= parent[1] + 2 - 0.5, "%s top %s" % (label, bbox)
        assert bbox[2] <= parent[2] - 2 + 0.5, "%s right %s" % (label, bbox)
        assert bbox[3] <= parent[3] - 2 + 0.5, "%s bottom %s" % (label, bbox)

    # art vs text: zero overlap (except texts flagged on_art)
    for bbox, parent, label, on_art in TEXTBOXES:
        if on_art:
            continue
        for rect, rlabel in ARTRECTS:
            ox = min(bbox[2], rect[2]) - max(bbox[0], rect[0])
            oy = min(bbox[3], rect[3]) - max(bbox[1], rect[1])
            assert not (ox > 0 and oy > 0), \
                "text %s overlaps art %s" % (label, rlabel)

    # card decks: max 2 lines
    for i, (region, head, deck, badge, key, bg) in enumerate(CARDS):
        dl = wrap(draw, deck, F(F_SANS, 10), cw[i % 5] - 14)
        assert len(dl) <= 2, "card %s deck %d lines" % (key, len(dl))
        hl = wrap(draw, head, F(F_SANS_B, 11), cw[i % 5] - 14)
        assert len(hl) <= 2, "card %s head %d lines" % (key, len(hl))

    # ALSO: one line each, no trailing preposition before the tag
    preps = {"of", "to", "in", "on", "at", "for", "by", "with", "from",
             "over", "after", "before", "amid", "vs", "per", "via", "into",
             "near", "off", "under", "about", "as", "and", "or", "the", "a"}
    for item in ALSO:
        assert draw.textlength("•  " + item, font=afont) <= colw, \
            "ALSO too long for one line: %s" % item
        core = item.rsplit("[", 1)[0].strip()
        assert core.split()[-1].lower().strip(",.;:") not in preps, \
            "ALSO ends with preposition: %s" % item
        assert item.rsplit("[", 1)[1].rstrip("]") in ("C", "R", "CL"), \
            "ALSO missing tag: %s" % item

    # DATE CHECK lines fit their box
    assert draw.textlength(line1, font=dfont) <= dp[2] - dp[0] - 20, \
        "datecheck line1 too long"
    assert draw.textlength(line2, font=dfont) <= dp[2] - dp[0] - 20, \
        "datecheck line2 too long"

    # pins: on land (mask pixel), whole circle inside the map panel,
    # pairwise centres >= 2r+2, 2-digit numbers
    for num, name, lon, lat in PINS:
        px, py = proj(lon, lat)
        assert mask.getpixel((int(px), int(py))) == 255, \
            "pin %s %s not on land (%.1f,%.1f)" % (num, name, lon, lat)
        assert MAP_X0 + 2 + pin_r <= px <= MAP_X1 - 2 - pin_r, \
            "pin %s x outside map" % num
        assert MAP_Y0 + 2 + pin_r <= py <= MAP_Y1 - 2 - pin_r, \
            "pin %s y outside map" % num
        assert len(num) == 2, "pin number must be 2 digits: %s" % num
    items = list(pin_xy.items())
    for a in range(len(items)):
        for b in range(a + 1, len(items)):
            (na, (xa, ya)), (nb, (xb, yb)) = items[a], items[b]
            d = ((xa - xb) ** 2 + (ya - yb) ** 2) ** 0.5
            assert d >= 2 * pin_r + 2, \
                "pins %s-%s too close: %.1f" % (na, nb, d)

    img.save(OUT, "PNG", optimize=True)
    data = open(OUT, "rb").read()
    print("entry.png %dx%d %d bytes sha256=%s" % (
        W, H, len(data), hashlib.sha256(data).hexdigest()))
    print("stories=50 heroes=3 cards=10 also=37 pins=12 datecheck=7")
    print("ALL ASSERTS PASSED")


if __name__ == "__main__":
    render()
