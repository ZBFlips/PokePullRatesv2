#!/usr/bin/env python3
"""
PullRates.gg — Automated Price Updater
Scrapes ThePriceDex for current card prices and writes prices.json.
Run via GitHub Actions every Sunday, or manually anytime.
"""

import json
import re
import time
import sys
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# ── Config ────────────────────────────────────────────────────
BASE_URL   = "https://www.thepricedex.com"
OUTPUT     = "prices.json"          # written relative to repo root
DELAY      = 2.5                    # seconds between requests (be polite)
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
# id: used in data.js   slug: used in ThePriceDex URLs
SETS = [
    # Mega Evolution
    { "id": "me2pt5",    "slug": "ascended-heroes"      },
    # Scarlet & Violet
    { "id": "sv9",       "slug": "journey-together"      },
    { "id": "sv8pt5",    "slug": "prismatic-evolutions"  },
    { "id": "sv8",       "slug": "surging-sparks"        },
    { "id": "sv7",       "slug": "stellar-crown"         },
    { "id": "sv6pt5",    "slug": "shrouded-fable"        },
    { "id": "sv6",       "slug": "twilight-masquerade"   },
    { "id": "sv5",       "slug": "temporal-forces"       },
    { "id": "sv4pt5",    "slug": "paldean-fates"         },
    { "id": "sv4",       "slug": "paradox-rift"          },
    { "id": "sv3pt5",    "slug": "pokemon-151"           },
    { "id": "sv3",       "slug": "obsidian-flames"       },
    { "id": "sv2",       "slug": "paldea-evolved"        },
    { "id": "sv1",       "slug": "scarlet-violet"        },
    # Sword & Shield
    { "id": "swsh12pt5", "slug": "crown-zenith"          },
    { "id": "swsh12",    "slug": "silver-tempest"        },
    { "id": "swsh11",    "slug": "lost-origin"           },
    { "id": "swsh7",     "slug": "evolving-skies"        },
]

# Map ThePriceDex rarity display names → our internal keys
RARITY_MAP = {
    # SV era
    "Mega Hyper Rare":         "MHR",
    "Hyper Rare":               "HR",
    "Special Illustration Rare":"SIR",
    "Mega Attack Rare":         "MAR",
    "Illustration Rare":        "IR",
    "ACE SPEC Rare":            "ACE",
    "Double Rare":              "DR",
    # Paldean Fates shinies
    "Shiny Rare":               "SHR",
    "Shiny Ultra Rare":         "SHU",
    # SWSH Trainer Gallery
    "TG Secret Rare":           "TGS",
    "Rainbow Rare":             "RBOW",
    "TG Ultra Rare":            "TGU",
    "TG Rare Holo VMAX":        "TGVM",
    "TG Rare Holo V":           "TGV",
    "TG Rare Holo":             "TGH",
    # SWSH Galarian Gallery (Crown Zenith)
    "GG Secret Rare":           "GGS",
    "GG Ultra Rare":            "GGU",
    "GG Rare Holo VSTAR":       "GGVS",
    "GG Rare Holo VMAX":        "TGVM",  # reuse key
    "GG Rare Holo V":           "TGV",   # reuse key
    "GG Rare Holo":             "TGH",   # reuse key
    # SWSH regular
    "Secret Rare":              "SR",
    "Rare Holo VSTAR":          "VSTAR",
    "Rare Holo VMAX":           "VMAX",
    "Rare Holo V":              "V",
    "Radiant Rare":             "RAD",
    "Rare Holo":                "RH",
    # Shared
    "Ultra Rare":               "UR",
    "Rare":                     "R",
    "Uncommon":                 "U",
    "Common":                   "C",
}


# ── HTTP helper ───────────────────────────────────────────────
def fetch(url, retries=MAX_RETRIES):
    """Fetch a URL and return the text content, with retries."""
    for attempt in range(retries):
        try:
            req = Request(url, headers=HEADERS)
            with urlopen(req, timeout=20) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except HTTPError as e:
            if e.code == 429:
                wait = 10 * (attempt + 1)
                print(f"    Rate limited, waiting {wait}s…")
                time.sleep(wait)
            elif e.code == 404:
                print(f"    404 Not Found: {url}")
                return None
            else:
                print(f"    HTTP {e.code}: {url} (attempt {attempt+1})")
                time.sleep(DELAY * 2)
        except URLError as e:
            print(f"    URL error: {e.reason} (attempt {attempt+1})")
            time.sleep(DELAY * 2)
        except Exception as e:
            print(f"    Unexpected error: {e} (attempt {attempt+1})")
            time.sleep(DELAY * 2)
    return None


# ── Parsers ───────────────────────────────────────────────────
def parse_price(text):
    """Parse '$123.45' or '$1,234' → float."""
    if not text:
        return None
    cleaned = re.sub(r"[^\d.]", "", text.replace(",", ""))
    try:
        return round(float(cleaned), 2)
    except (ValueError, TypeError):
        return None


def parse_pull_rates_page(html):
    """
    Extract from the EV breakdown table:
      { rarity_key: { avgPrice, ev }, ... }
    and the pack EV from the header stat.
    """
    if not html:
        return {}, None

    results = {}
    pack_ev = None

    # ── Pack EV ───────────────────────────────────────────────
    ev_match = re.search(
        r"Booster Pack EV\s*#{3,6}\s*\$?([\d,]+\.?\d*)",
        html, re.IGNORECASE
    )
    if ev_match:
        pack_ev = parse_price(ev_match.group(1))

    # ── EV breakdown table ────────────────────────────────────
    # Table rows look like: | Rarity Name | N | N | $X.XX | $X.XX |
    # We grab the rarity name and avg value column
    row_pattern = re.compile(
        r"\|\s*([^|]+?)\s*\|\s*\d+\s*\|\s*\d+\s*\|\s*\$?([\d,]+\.?\d*)\s*\|\s*\$?([\d,]+\.?\d*)\s*\|"
    )
    for m in row_pattern.finditer(html):
        rarity_name = m.group(1).strip()
        avg_price_str = m.group(2).strip()
        ev_str = m.group(3).strip()

        # Skip header rows and total row
        if rarity_name.lower() in ("rarity", "total", ""):
            continue
        # Skip reverse / energy rows
        if "reverse" in rarity_name.lower() or "energy" in rarity_name.lower():
            continue

        key = RARITY_MAP.get(rarity_name)
        if not key:
            # Try partial match
            for display, k in RARITY_MAP.items():
                if display.lower() in rarity_name.lower():
                    key = k
                    break
        if not key:
            continue

        avg_price = parse_price(avg_price_str)
        ev        = parse_price(ev_str)
        if avg_price is not None:
            results[key] = {
                "avgPrice": avg_price,
                "ev":       ev if ev is not None else 0,
            }

    return results, pack_ev


def parse_top_cards_page(html):
    """
    Extract individual card prices from the most-expensive guide page.
    Returns { card_name_lower: price, ... }
    """
    if not html:
        return {}

    prices = {}

    # Pattern: card name heading followed by price heading
    # e.g.  ## Charizard ex#234 Holo\n##### $216.81
    card_blocks = re.finditer(
        r"##\s+([^\n#$]+?)(?:#\d+[^\n]*)?\n+#{3,6}\s*\$?([\d,]+\.?\d*)",
        html
    )
    for m in card_blocks:
        name  = m.group(1).strip()
        price = parse_price(m.group(2))
        if price and price > 0.50:   # ignore bulk cards
            # Normalise name for fuzzy matching
            key = re.sub(r"\s+", " ", name.lower().strip())
            prices[key] = price

    return prices


def match_notable_prices(notable_names, top_card_prices):
    """
    For each notable card name in our data.js, find the best price match
    from the scraped top_card_prices dict.
    Returns { original_name: price }
    """
    matched = {}
    for name in notable_names:
        norm = re.sub(r"\s+", " ", name.lower().strip())
        # Exact match first
        if norm in top_card_prices:
            matched[name] = top_card_prices[norm]
            continue
        # Partial match: our name contained in scraped name
        best_price = None
        for scraped_name, price in top_card_prices.items():
            if norm in scraped_name or scraped_name in norm:
                best_price = price
                break
        if best_price:
            matched[name] = best_price

    return matched


# ── Main ──────────────────────────────────────────────────────
def main():
    print(f"\n{'='*55}")
    print(f"  PullRates.gg Price Updater — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{'='*55}\n")

    # Load existing prices.json as fallback
    try:
        with open(OUTPUT, "r") as f:
            existing = json.load(f)
        print(f"Loaded existing {OUTPUT} as fallback.\n")
    except (FileNotFoundError, json.JSONDecodeError):
        existing = {"sets": {}}
        print(f"No existing {OUTPUT} found — starting fresh.\n")

    new_data = {
        "lastUpdated": datetime.now(timezone.utc).strftime("%B %-d, %Y"),
        "sets": {}
    }

    failed_sets = []

    for set_def in SETS:
        sid   = set_def["id"]
        slug  = set_def["slug"]
        print(f"  [{sid}] {slug}")

        # 1. Fetch pull rates page
        pull_url = f"{BASE_URL}/set/{sid}/{slug}/pull-rates"
        print(f"    → Fetching pull rates…")
        pull_html = fetch(pull_url)
        time.sleep(DELAY)

        rarity_prices, pack_ev = parse_pull_rates_page(pull_html)
        if not rarity_prices:
            print(f"    ⚠ Could not parse rarity prices — using fallback")
            rarity_prices = existing.get("sets", {}).get(sid, {}).get("rarities", {})
            pack_ev = existing.get("sets", {}).get(sid, {}).get("packEV")
            failed_sets.append(sid)

        # 2. Fetch top cards guide
        guide_url = f"{BASE_URL}/guides/most-expensive-{slug}-cards"
        print(f"    → Fetching top cards…")
        guide_html = fetch(guide_url)
        time.sleep(DELAY)

        top_card_prices = parse_top_cards_page(guide_html)
        print(f"    → Found {len(top_card_prices)} notable card prices")

        # 3. Get notable card names from existing prices.json or use empty list
        existing_set = existing.get("sets", {}).get(sid, {})
        notable_names = list(existing_set.get("notablePrices", {}).keys())

        # Match notable prices
        notable_prices = match_notable_prices(notable_names, top_card_prices)

        # Also store top card data (name + price of most expensive)
        top_card = None
        if top_card_prices:
            top_name, top_price = max(top_card_prices.items(), key=lambda x: x[1])
            top_card = { "name": top_name.title(), "price": top_price }

        # 4. Assemble set entry
        entry = {
            "rarities":      rarity_prices,
            "notablePrices": notable_prices or existing_set.get("notablePrices", {}),
            "topCard":       top_card or existing_set.get("topCard"),
        }
        if pack_ev:
            entry["packEV"] = pack_ev

        new_data["sets"][sid] = entry

        if rarity_prices:
            ev_str = f"  (packEV ${pack_ev})" if pack_ev else ""
            print(f"    ✓ {len(rarity_prices)} rarities updated{ev_str}")
        print()

    # Write output
    with open(OUTPUT, "w") as f:
        json.dump(new_data, f, indent=2)

    print(f"\n{'='*55}")
    print(f"  ✅ prices.json updated — {len(new_data['sets'])} sets")
    if failed_sets:
        print(f"  ⚠  Fallback used for: {', '.join(failed_sets)}")
    print(f"{'='*55}\n")

    # Exit with error code if more than half failed (so GitHub Action can flag it)
    if len(failed_sets) > len(SETS) / 2:
        sys.exit(1)


if __name__ == "__main__":
    main()
