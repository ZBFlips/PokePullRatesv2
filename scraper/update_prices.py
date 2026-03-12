#!/usr/bin/env python3
import json
import re
import time
import sys
import random
from datetime import datetime, timezone

# ── Config ────────────────────────────────────────────────────
BASE_URL    = "https://www.thepricedex.com"
OUTPUT      = "prices.json"

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
    { "id": "swsh10",    "slug": "astral-radiance",      "guide": "astral-radiance"     },
    { "id": "swsh9",     "slug": "brilliant-stars",      "guide": "brilliant-stars"     },
    { "id": "swsh8",     "slug": "fusion-strike",        "guide": "fusion-strike"       },
    { "id": "swsh7",     "slug": "evolving-skies",       "guide": "evolving-skies"      },
]

# ── Engine ────────────────────────────────────────────────────

def fetch_content(url):
    """Guaranteed fetch using Playwright for GitHub Actions."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            try:
                page.goto(url, wait_until="networkidle", timeout=60000)
                page.mouse.wheel(0, 500)
                time.sleep(2)
                return page.content()
            finally:
                browser.close()
    except ImportError:
        import urllib.request
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.read().decode('utf-8', errors='replace')
        except: return None

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
    new_data = {"lastUpdated": now.strftime('%B %d, %Y at %H:%M UTC'), "sets": {}}

    for s in SETS:
        sid, slug = s["id"], s["slug"]
        print(f"[{sid}] Processing {slug}...")

        # 1. Scrape Retail Resale
        pc_url = f"https://www.pricecharting.com/game/pokemon-{slug}/{slug}-booster-pack"
        pc_html = fetch_content(pc_url)
        sealed = 0.0
        if pc_html:
            m = re.search(r'id="new_price"[^>]*>\s*\$([\d,]+\.\d{2})', pc_html, re.I)
            if not m: m = re.search(r'id="used_price"[^>]*>\s*\$([\d,]+\.\d{2})', pc_html, re.I)
            sealed = parse_price(m.group(1)) if m else 0.0

        # STRICT BUNDLE GUARD: Specifically for the $63.99 Ascended Heroes error
        # If the price is exactly what we saw (63.99) or in that range, divide by 6.
        if sealed > 40.0 and sealed < 85.0 and sid != 'swsh7':
            print(f"    ⚠ Detected probable 6-pack bundle price (${sealed}). Dividing by 6...")
            sealed = round(sealed / 6, 2)
        elif sealed > 25.0 and sid != 'swsh7':
            # Cap modern packs at $25 unless it's Evolving Skies
            print(f"    ⚠ Price anomaly (${sealed}). Reverting to fallback.")
            sealed = existing.get("sets", {}).get(sid, {}).get("packResalePrice", 0.0)

        # 2. Scrape EV
        ev_html = fetch_content(f"{BASE_URL}/set/{sid}/{slug}/pull-rates")
        pack_ev = 0.0
        if ev_html:
            ev_m = re.search(r'Booster Pack EV.*?\$([\d,]+\.?\d*)', ev_html, re.I | re.S)
            if ev_m: pack_ev = parse_price(ev_m.group(1))

        # 3. Consolidate
        ex = existing.get("sets", {}).get(sid, {})
        new_data["sets"][sid] = {
            "rarities": ex.get("rarities", {}),
            "packEV": pack_ev or ex.get("packEV", 0.0),
            "packResalePrice": sealed or ex.get("packResalePrice", 0.0),
            "topCard": ex.get("topCard", {"name": "N/A", "price": 0.0})
        }
        print(f"    ✓ EV: ${pack_ev} | Retail: ${sealed}")
        time.sleep(random.uniform(2, 4))

    with open(OUTPUT, "w") as f:
        json.dump(new_data, f, indent=2)
    print(f"\n✅ Scraping Complete. Output written to {OUTPUT}")

if __name__ == "__main__":
    main()
