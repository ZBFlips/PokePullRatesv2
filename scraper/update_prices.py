#!/usr/bin/env python3
import json
import re
import time
import sys
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

# ── Config ────────────────────────────────────────────────────
BASE_URL    = "https://www.thepricedex.com"
OUTPUT      = "prices.json"

# Safety Net: Hardcoded fallbacks if the internet fails
BASE_PRICES = {
    "me2pt5": 14.25, "sv9": 4.50, "sv8pt5": 5.25, "sv8": 3.99,
    "sv7": 3.95, "sv6pt5": 4.50, "sv6": 3.85, "sv5": 3.75,
    "sv4pt5": 4.95, "sv4": 3.50, "sv3pt5": 10.50, "sv3": 3.50
}

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
    { "id": "sv3",       "slug": "obsidian-flames",      "guide": "obsidian-flames"     }
]

# ── Foolproof Browser Engine ───────────────────────────────────

def get_page_data(url):
    """Uses a real headless browser to render JavaScript and bypass blocks."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            return page.content()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
        finally:
            browser.close()

def parse_price(text):
    if not text: return 0.0
    cleaned = re.sub(r"[^\d.]", "", str(text).replace(",", ""))
    try: return round(float(cleaned), 2)
    except: return 0.0

# ── Main ──────────────────────────────────────────────────────

def main():
    try:
        with open(OUTPUT) as f: existing = json.load(f)
    except: existing = {"sets": {}}

    now = datetime.now(timezone.utc)
    new_data = {
        "lastUpdated": now.strftime('%B %d, %Y at %H:%M UTC'),
        "sets": {}
    }

    for s in SETS:
        sid, slug = s["id"], s["slug"]
        print(f"[{sid}] Scraping {slug}...")

        # 1. Fetch Pull Rates Page
        html = get_page_data(f"{BASE_URL}/set/{sid}/{slug}/pull-rates")
        
        # Simple extraction for demo - replace with your specific token scanning
        pack_ev = 0.0
        if html:
            ev_m = re.search(r'Booster Pack EV.*?\$([\d,]+\.?\d*)', html, re.I | re.S)
            if ev_m: pack_ev = parse_price(ev_m.group(1))

        # 2. Fetch Sealed Price from PriceCharting
        pc_url = f"https://www.pricecharting.com/game/pokemon-{slug}/booster-pack"
        pc_html = get_page_data(pc_url)
        sealed = 0.0
        if pc_html:
            m = re.search(r'id="used_price"[^>]*>\s*\$([\d,]+\.?\d*)', pc_html, re.I)
            sealed = parse_price(m.group(1)) if m else 0.0

        # Implementation of Fallbacks
        if sealed == 0.0:
            sealed = BASE_PRICES.get(sid, 0.0)
            print(f"    ! Using fallback for sealed price: ${sealed}")

        new_data["sets"][sid] = {
            "rarities": {}, # Add your rarity parsing logic here
            "packEV": pack_ev,
            "packResalePrice": sealed,
            "topCard": {"name": "N/A", "price": 0.0}
        }
        print(f"    ✓ EV: ${pack_ev} | Resale: ${sealed}")

    with open(OUTPUT, "w") as f:
        json.dump(new_data, f, indent=2)
    print("\n✅ Update Complete.")

if __name__ == "__main__":
    main()
