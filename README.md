# news-26-b167-numbers — The World in One Day (Thursday 26 November 2026)

[![News Image 20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![Rank](https://make.fun/badge/news-image-20261126/akbare12/news-26-b167-numbers/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![Reward](https://make.fun/badge/news-image-20261126/akbare12/news-26-b167-numbers/reward.svg)](https://make.fun/bounty/news-image-20261126)

One image summing up the world's news of **Thursday 26 November 2026**:
50 stories across 10 regions — 3 heroes, 10 cards, 37 more in ALSO.

**Heroes:** Macy's 100th Thanksgiving Parade postponed by storm (a first
ever for weather) · Iran claims 2 tankers hit by mines in the Strait of
Hormuz · global markets rebound as Trump's tariff salvo lands softer
than feared. A 12-pin world map, and a DATE CHECK footer that names
7 stories deliberately excluded because they happened on other days.

## Revision — 27 Nov 2026 (coordinator zoom-check fixes)

- DATE CHECK is now exactly these 7 verbatim items: COP31 failed 22 Nov ·
  Shenzhou-24 launched 25 Nov · Cairo tanker blast, 31 dead, 25 Nov ·
  Cartagena hostages freed 25 Nov · Australia-Solomon pact 25 Nov ·
  UK energy prices +26% announced 25 Nov · Huawei convicted 24 Nov.
- Hero 2 deck no longer mixes the IRGC mine claim with the UKMTO Khasab
  incident: "hit sea mines in the Strait. The claim is unverified."
- The ALSO item duplicating the Bogor card was replaced by "Duran Duran
  guitarist Andy Taylor dies aged 65 [C]" (announced 25 Nov).
- Kyiv deck now reads "113 drones overnight" (not "in reply"); gold is
  "down 0.2% on Thursday" per kanon. "Dollar flat at 103.71 [C]" was
  verified live against Reuters (DXY flat at 103.7 / 103.71, 26 Nov).

## Verification (entry.png after this revision)

- `entry.png` 1024×1024, 157,755 bytes,
  sha256 `e83a40a430c2a3a985174fd986640d5a434bcd3fe70205916e2437d6b20e9540`
- `python3 gen.py`: ALL ASSERTS PASSED (ALSO 37, DATE CHECK exact-list
  match, hero-2 deck free of "near Khasab", Bogor exactly once as a card).
- Stdlib-venv simulation: exit 0, output sha256 matches entry.png.
- Visual check: full image + 2× crops of ALSO, map, DATE CHECK and
  heroes read as images — DATE CHECK is exactly the 7 items above,
  hero-2 deck is clean, Bogor appears once.

## Layout — V163 ATLAS BANNER

Masthead band with the date · 3 hero columns, each with its own
geometric scene and a WHY IT MATTERS line · 10 cards in 5×2, each with
a scene strip and a number badge · full-width world-map strip with
12 numbered pins (Java sits in South-East Asia above Australia) ·
3-column ALSO list (37 items) · 2-line DATE CHECK footer (7 items).

## How it works

- `gen.py` (Pillow, build-time only) renders `entry.png` (1024×1024).
- `main.py` (stdlib only: `os` + `shutil`) copies `entry.png` into
  `$MAKEFUN_OUTPUT_DIR/entry.png`. The grader is stdlib-only, so
  `main.py` imports nothing else.

## Build

```sh
python3 gen.py        # renders entry.png + runs all layout asserts
python3 main.py       # copies entry.png to $MAKEFUN_OUTPUT_DIR (or out/)
```

`gen.py` asserts before saving: ALSO is exactly 37, pins are 12 and all
on land (pixel-checked), pin circles are whole and spaced, card decks
are at most 2 lines, no text overlaps art, all text sits inside its
parent box, DATE CHECK matches its 7-item verbatim list exactly (not
just a count), the hero-2 deck contains no "near Khasab", Bogor occurs
exactly once (as a card, never in ALSO), every card deck and every ALSO
item carries a literal [C]/[R]/[CL] tag, ALSO font is 10 px.

Verify the stdlib-only run like the grader does (fresh venv, no Pillow,
different cwd, empty out dir, read-only repo copy):

```sh
python3 -m venv ~/workspace/makefun/sim-b167-venv
MAKEFUN_OUTPUT_DIR=/path/to/empty/out \
  ~/workspace/makefun/sim-b167-venv/bin/python main.py
```

## Entry

- Bounty: [news-image-20261126](https://make.fun/bounty/news-image-20261126)
- Repo: `akbare12/news-26-b167-numbers`
