# The World Today — 22 November 2026

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/news-image-20261122)
[![date](https://img.shields.io/badge/date-22%20November%202026-red)](https://make.fun/bounty/news-image-20261122)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A newspaper front page summing up world news of **Sunday 22 November 2026**,
drawn with PIL by `draw-news-image-20261122.py`. `main.py` (standard library
only) copies the baked `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` after
validating it: PNG magic, at most 1024×1024 pixels, at most 1 MiB.

## The four stories

1. **Gulf escalation — Iran strikes US bases in Bahrain.** Iran's IRGC says
   missiles and drones hit two US Patriot air-defence radars at the al-Riffa
   and Awali bases late on Saturday. Bahrain says an Iranian attack set a
   civilian industrial site on fire; no casualties were reported, and the US
   has not confirmed damage to its equipment. (Al Jazeera / ANI, Reuters)
2. **COP31 tables new text after overtime.** Climate talks in Antalya,
   Turkey, ran past their Friday deadline; a new deal text was tabled in the
   early hours of Sunday, with an approval session due on Sunday morning.
   Fossil-fuel wording was the sticking point. (Reuters)
3. **France — fourth weekend of cost-of-living protests.** Nationwide
   demonstrations over rising prices entered a fourth consecutive weekend.
   (The Paris Eye)
4. **Myanmar — magnitude 4.1 quake.** An earthquake of magnitude 4.1 struck
   Myanmar in the early hours of Sunday, reported by India's National Centre
   for Seismology. (ANI)

## Run it

```sh
python3 draw-news-image-20261122.py   # re-render entry.png (deterministic)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Bounty: https://make.fun/bounty/news-image-20261122
