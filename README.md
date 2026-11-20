[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/andikusumah78/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/andikusumah78/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

# news-image-20261120 — The World in One Page

One image summing up Friday 20 November 2026's world news, drawn as a
newspaper front page:

- **Shenzhen — Three leaders sign a 'peace declaration'.** Trump, Putin and
  Xi hold the first-ever trilateral summit and agree a four-point pact: UN
  reform, more oil supply, curbs on the ICC, and a pledge that nuclear war
  "must never be fought". Ukraine and Iran are not mentioned.
- **Brussels — 100,000 a year.** The UK and EU agree a youth mobility
  scheme: 100,000 places a year, each way.
- **Taipei — Markets plunge 6.2%.** Taiwan stocks cap their worst week since
  1991 as the AI trade unwinds; TSMC falls below NT$2,000.
- **Kyiv — Missiles hit Kyiv.** Ballistic strikes hit bridges in the
  capital; the Austrian and Dutch embassies are damaged.

## How it works

`tools/make_image.py` draws the front page programmatically with Pillow (no
photos, no external assets). `main.py` (Python 3.13 standard library only)
copies `assets/entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, verifying the
PNG header, dimensions (1024x1024) and size (under 1 MiB) before and after
the copy. Two runs produce byte-identical output.

## Run it

```sh
python3 tools/make_image.py            # re-render assets/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py # write out/entry.png
```

Entry for the [make.fun bounty](https://make.fun/bounty/news-image-20261120)
"Sum up 20 November's world news in one image" (pot $250, top 50 share it).
