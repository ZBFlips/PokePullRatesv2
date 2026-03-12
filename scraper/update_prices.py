#!/usr/bin/env python3
"""
PullRates.gg — Automated Price Updater
Scrapes ThePriceDex for current card prices and writes prices.json.
Run via GitHub Actions every Sunday, or manually anytime.
Uses only Python stdlib — no pip installs required.
"""

import json
import re
import time
import sys
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser

# ── Config ────────────────────────────────────────────────────
BASE_URL    = "https://www.thepricedex.com"
OUTPUT      = "prices.json"
DELAY       = 3.0
MAX_RETRIES = 3
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# ── Set definitions ───────────────────────────────────────────
# guide: the slug used in /guides/most-expensive-{guide}-cards
SETS = [
    { "id": "me2pt5",    "slug": "ascended-heroes",     "guide": "ascended-heroes"     },
    { "id": "sv9",       "slug": "journey-together",     "guide": "journey-together"    },
    { "id": "sv8pt5",    "slug": "prismatic-evolutions", "guide": "prismatic-evolutions"},
    { "id": "sv8",       "slug": "surging-sparks",       "guide": "surging-sparks"      },
    { "id": "sv7",       "slug": "stellar-crown",        "guide": "stellar-crown"       },
    { "id": "sv6pt5",    "slug": "shrouded-fable",       "guide": "shrouded-fable"      },
    { "id": "sv6",       "slug": "twilight-masquerade",  "guide": "twilight-masquerade" },
    { "id": "sv5",       "slug": "temporal-forces",      "guide": "temporal-forces"     },
    { "id": "sv4pt5",    "slug": "paldean-fates",        "guide": "paldean-fates"       },
    { "id": "sv4",       "slug": "paradox-rift",         "guide": "paradox-rift"        },
    { "id": "sv3pt5",    "slug": "pokemon-151",          "guide": "151"                 },
    { "id": "sv3",       "slug": "obsidian-flames",      "guide": "obsidian-flames"     },
    { "id": "sv2",       "slug": "paldea-evolved",       "guide": "paldea-evolved"      },
    { "id": "sv1",       "slug": "scarlet-violet",       "guide": "scarlet-violet"      },
    { "id": "swsh12pt5", "slug": "crown-zenith",         "guide": "crown-zenith"        },
    { "id": "swsh12",    "slug": "silver-tempest",       "guide": "silver-tempest"      },
    { "id": "swsh11",    "slug": "lost-origin",          "guide": "lost-origin"         },
    { "id": "swsh7",     "slug": "evolving-skies",       "guide": "evolving-skies"      },
]

RARITY_MAP = {
    "mega hyper rare":           "MHR",
    "hyper rare":                "HR",
    "special illustration rare": "SIR",
    "mega attack rare":          "MAR",
    "illustration rare":         "IR",
    "ace spec rare":             "ACE",
    "double rare":               "DR",
    "shiny rare":                "SHR",
    "shiny ultra rare":          "SHU",
    "tg secret rare":            "TGS",
    "rainbow rare":              "RBOW",
    "tg ultra rare":             "TGU",
    "tg rare holo vmax":         "TGVM",
    "tg rare holo v":            "TGV",
    "tg rare holo":              "TGH",
    "gg secret rare":            "GGS",
    "gg ultra rare":             "GGU",
    "gg rare holo vstar":        "GGVS",
    "gg rare holo vmax":         "TGVM",
    "gg rare holo v":            "TGV",
    "gg rare holo":              "TGH",
    "secret rare":               "SR",
    "rare holo vstar":           "VSTAR",
    "rare holo vmax":            "VMAX",
    "rare holo v":               "V",
    "radiant rare":              "RAD",
    "rare holo":                 "RH",
    "ultra rare":                "UR",
    "rare":                      "R",
    "uncommon":                  "U",
    "common":                    "C",
}

SKIP = {"energy", "total", "rarity", ""}


# ── HTML Parsers ──────────────────────────────────────────────

class TableParser(HTMLParser):
    """Extracts all HTML tables as list-of-rows, each row a list of cell strings."""

    def __init__(self):
        super().__init__()
        self.tables    = []
        self._table    = None
        self._row      = None
        self._cell     = None
        self._in_cell  = False

    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        if t == "table":
            self._table = []
        elif t == "tr" and self._table is not None:
            self._row = []
        elif t in ("td", "th") and self._row is not None:
            self._cell   = []
            self._in_cell = True

    def handle_endtag(self, tag):
        t = tag.lower()
        if t == "table" and self._table is not None:
            self.tables.append(self._table)
            self._table = None
        elif t == "tr" and self._row is not None:
            if self._table is not None:
                self._table.append(self._row)
            self._row = None
        elif t in ("td", "th") and self._in_cell:
            text = " ".join("".join(self._cell).split())
            if self._row is not None:
                self._row.append(text)
            self._cell   = None
            self._in_cell = False

    def handle_data(self, data):
        if self._in_cell and self._cell is not None:
            self._cell.append(data)

    def handle_entityref(self, name):
        if self._in_cell and self._cell is not None:
            self._cell.append({"amp":"&","lt":"<","gt":">","nbsp":" ",
                                "quot":'"',"apos":"'"}.get(name, ""))

    def handle_charref(self, name):
        if self._in_cell and self._cell is not None:
            try:
                ch = chr(int(name[1:], 16) if name.startswith("x") else int(name))
                self._cell.append(ch)
            except Exception:
                pass


class CardPriceParser(HTMLParser):
    """
    Parses guide pages. Card names are in <h2> tags; prices in <h5> tags.
    Pairs them up sequentially.
    """

    def __init__(self):
        super().__init__()
        self.prices     = {}   # { lower_name: price }
        self._tag       = None
        self._buf       = []
        self._last_name = None

    def handle_starttag(self, tag, attrs):
        t = tag.lower()
        if t in ("h1","h2","h3","h4","h5","h6"):
            self._tag = t
            self._buf = []

    def handle_endtag(self, tag):
        t = tag.lower()
        if t != self._tag:
            return
        text = " ".join("".join(self._buf).split()).strip()
        self._tag = None
        self._buf = []

        if not text:
            return

        if t == "h2":
            # Strip trailing "#123 Holo" card-number suffix
            name = re.sub(r"#\S.*$", "", text).strip()
            name = re.sub(r"\s+Holo\s*$", "", name, flags=re.I).strip()
            if name:
                self._last_name = name

        elif t in ("h5", "h4") and self._last_name:
            price = parse_price(text)
            if price and price >= 0.50:
                key = re.sub(r"\s+", " ", self._last_name.lower().strip())
                if key not in self.prices:   # keep the first (highest rank = most exp)
                    self.prices[key] = price
            self._last_name = None   # consume the name regardless

    def handle_data(self, data):
        if self._tag:
            self._buf.append(data)

    def handle_entityref(self, name):
        if self._tag:
            self._buf.append({"amp":"&","lt":"<","gt":">","nbsp":" ",
                              "quot":'"',"apos":"'"}.get(name, ""))

    def handle_charref(self, name):
        if self._tag:
            try:
                ch = chr(int(name[1:], 16) if name.startswith("x") else int(name))
                self._buf.append(ch)
            except Exception:
                pass


# ── Helpers ───────────────────────────────────────────────────

def parse_price(text):
    if not text:
        return None
    cleaned = re.sub(r"[^\d.]", "", str(text).replace(",", ""))
    try:
        v = float(cleaned)
        return round(v, 2) if v > 0 else None
    except (ValueError, TypeError):
        return None


def fetch(url, retries=MAX_RETRIES):
    for attempt in range(retries):
        try:
            req = Request(url, headers=HEADERS)
            with urlopen(req, timeout=25) as resp:
                raw = resp.read()
                enc = resp.info().get("Content-Encoding", "")
                if enc == "gzip":
                    import gzip
                    raw = gzip.decompress(raw)
                elif enc == "br":
                    # brotli rarely used without extra lib; just try decode
                    pass
                return raw.decode("utf-8", errors="replace")
        except HTTPError as e:
            if e.code == 404:
                print(f"      404: {url}")
                return None
            if e.code == 429:
                wait = 15 * (attempt + 1)
                print(f"      Rate limited — waiting {wait}s…")
                time.sleep(wait)
            else:
                print(f"      HTTP {e.code} (attempt {attempt+1})")
                time.sleep(DELAY * 2)
        except URLError as e:
            print(f"      URLError: {e.reason} (attempt {attempt+1})")
            time.sleep(DELAY * 2)
        except Exception as e:
            print(f"      Error: {e} (attempt {attempt+1})")
            time.sleep(DELAY * 2)
    return None


def parse_pull_rates_page(html):
    """Returns (rarity_prices dict, pack_ev float|None)."""
    if not html:
        return {}, None

    # Pack EV — scan raw text for the stat block
    pack_ev = None
    ev_m = re.search(
        r"Booster\s+Pack\s+EV[^$\d]{0,60}\$([\d,]+\.?\d*)",
        html, re.IGNORECASE | re.DOTALL
    )
    if ev_m:
        pack_ev = parse_price(ev_m.group(1))

    # Parse tables
    tp = TableParser()
    tp.feed(html)

    rarity_prices = {}

    for table in tp.tables:
        if len(table) < 2:
            continue

        header = [c.lower().strip() for c in table[0]]

        # We want the EV breakdown table: has "avg value" and "ev/pack" columns
        has_avg = any("avg" in h and "value" in h for h in header)
        has_ev  = any("ev" in h and "pack" in h for h in header)
        if not (has_avg and has_ev):
            continue

        # Find column positions
        def col(needle_fn):
            for i, h in enumerate(header):
                if needle_fn(h):
                    return i
            return None

        rarity_col = col(lambda h: "rarity" in h)
        price_col  = col(lambda h: "avg" in h and "value" in h)
        ev_col     = col(lambda h: "ev" in h and "pack" in h)

        if None in (rarity_col, price_col, ev_col):
            continue

        for row in table[1:]:
            if len(row) <= max(rarity_col, price_col, ev_col):
                continue

            rarity_raw = row[rarity_col].strip()
            rarity_lo  = rarity_raw.lower()

            # Skip unwanted rows
            if rarity_lo in SKIP:
                continue
            if any(x in rarity_lo for x in ("reverse", "energy", "total", "---", "priced")):
                continue

            key = RARITY_MAP.get(rarity_lo)
            if not key:
                for display, k in RARITY_MAP.items():
                    if display in rarity_lo:
                        key = k
                        break
            if not key:
                continue

            avg_price = parse_price(row[price_col])
            ev        = parse_price(row[ev_col])
            if avg_price is not None:
                rarity_prices[key] = {
                    "avgPrice": avg_price,
                    "ev":       ev or 0,
                }

    return rarity_prices, pack_ev


def parse_guide_page(html):
    if not html:
        return {}
    p = CardPriceParser()
    p.feed(html)
    return p.prices


def match_notable_prices(notable_names, top_card_prices):
    matched = {}
    for name in notable_names:
        norm = re.sub(r"\s+", " ", name.lower().strip())
        if norm in top_card_prices:
            matched[name] = top_card_prices[norm]
            continue
        for scraped, price in top_card_prices.items():
            if norm in scraped or scraped in norm:
                matched[name] = price
                break
    return matched


# ── Main ──────────────────────────────────────────────────────

def main():
    print(f"\n{'='*55}")
    print(f"  PullRates.gg — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*55}\n")

    try:
        with open(OUTPUT) as f:
            existing = json.load(f)
        print(f"Loaded existing {OUTPUT} as fallback.\n")
    except (FileNotFoundError, json.JSONDecodeError):
        existing = {"sets": {}}
        print("No existing prices.json — starting fresh.\n")

    new_data = {
        "lastUpdated": datetime.now(timezone.utc).strftime("%B %-d, %Y"),
        "sets": {}
    }
    failed = []

    for s in SETS:
        sid, slug, guide_slug = s["id"], s["slug"], s["guide"]
        print(f"  [{sid}] {slug}")

        # Pull rates
        pull_html = fetch(f"{BASE_URL}/set/{sid}/{slug}/pull-rates")
        time.sleep(DELAY)
        rarity_prices, pack_ev = parse_pull_rates_page(pull_html)

        if not rarity_prices:
            print(f"    ⚠ Parse failed — using fallback")
            ex = existing.get("sets", {}).get(sid, {})
            rarity_prices = ex.get("rarities", {})
            if not pack_ev:
                pack_ev = ex.get("packEV")
            failed.append(sid)
        else:
            print(f"    ✓ {len(rarity_prices)} rarities  packEV=${pack_ev}")

        # Guide page
        guide_html = fetch(f"{BASE_URL}/guides/most-expensive-{guide_slug}-cards")
        time.sleep(DELAY)
        top_card_prices = parse_guide_page(guide_html)
        print(f"    ✓ {len(top_card_prices)} notable prices")

        # Notable matching
        ex = existing.get("sets", {}).get(sid, {})
        notable_names  = list(ex.get("notablePrices", {}).keys())
        notable_prices = match_notable_prices(notable_names, top_card_prices)

        top_card = ex.get("topCard")
        if top_card_prices:
            top_name, top_price = max(top_card_prices.items(), key=lambda x: x[1])
            top_card = {"name": top_name.title(), "price": top_price}

        entry = {
            "rarities":      rarity_prices,
            "notablePrices": notable_prices or ex.get("notablePrices", {}),
            "topCard":       top_card,
        }
        if pack_ev:
            entry["packEV"] = pack_ev

        new_data["sets"][sid] = entry
        print()

    with open(OUTPUT, "w") as f:
        json.dump(new_data, f, indent=2)

    print(f"\n{'='*55}")
    print(f"  ✅ prices.json written — {len(new_data['sets'])} sets")
    if failed:
        print(f"  ⚠  Fallback used for: {', '.join(failed)}")
    print(f"{'='*55}\n")

    if len(failed) > len(SETS) / 2:
        sys.exit(1)


if __name__ == "__main__":
    main()
