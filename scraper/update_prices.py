#!/usr/bin/env python3
import json
import re
import time
import sys
import random
from datetime import datetime, timezone
from html.parser import HTMLParser

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
    { "id": "sv3",       "slug": "obsidian-flames",      "guide": "obsidian-flames"     }
]

# ── Engine ────────────────────────────────────────────────────

def fetch_content(url):
    """
    Tries Playwright for a real browser render. 
    Falls back to Urllib if running on a machine without Playwright.
    """
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
            page = context.new_page()
            try:
                page.goto(url, wait_until="networkidle", timeout=60000)
                # Mimic human scroll to trigger lazy-loaded price elements
                page.mouse.wheel(0, 500)
                time.sleep(2)
                return page.content()
            finally:
                browser.close()
    except ImportError:
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
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
    new_data = {
        "lastUpdated": now.strftime('%B %d, %Y at %H:%M UTC'),
        "sets": {}
    }

    for s in SETS:
        sid, slug = s["id"], s["slug"]
        print(f"[{sid}] Processing {slug}...")

        # 1. Scrape Retail Resale (PriceCharting)
        pc_url = f"https://www.pricecharting.com/game/pokemon-{slug}/{slug}-booster-pack"
        pc_html = fetch_content(pc_url)
        sealed = 0.0
        
        if pc_html:
            # Multi-Stage Search: Check 'New' (Retail) -> 'Used' (Market) -> Global find
            m = re.search(r'id="new_price"[^>]*>\s*\$([\d,]+\.\d{2})', pc_html, re.I)
            if not m:
                m = re.search(r'id="used_price"[^>]*>\s*\$([\d,]+\.\d{2})', pc_html, re.I)
            if not m:
                m = re.search(r'Ungraded.*?\$([\d,]+\.\d{2})', pc_html, re.I | re.S)
            
            sealed = parse_price(m.group(1)) if m else 0.0

        # 2. Scrape EV (ThePriceDex)
        ev_html = fetch_content(f"{BASE_URL}/set/{sid}/{slug}/pull-rates")
        pack_ev = 0.0
        if ev_html:
            ev_m = re.search(r'Booster Pack EV.*?\$([\d,]+\.?\d*)', ev_html, re.I | re.S)
            if ev_m: pack_ev = parse_price(ev_m.group(1))

        # 3. Consolidate and Save
        ex = existing.get("sets", {}).get(sid, {})
        new_data["sets"][sid] = {
            "rarities": ex.get("rarities", {}),
            "packEV": pack_ev or ex.get("packEV", 0.0),
            "packResalePrice": sealed or ex.get("packResalePrice", 0.0),
            "topCard": ex.get("topCard", {"name": "N/A", "price": 0.0})
        }
        print(f"    ✓ EV: ${pack_ev} | Retail: ${sealed}")
        
        # Anti-ban jitter
        time.sleep(random.uniform(2, 4))

    with open(OUTPUT, "w") as f:
        json.dump(new_data, f, indent=2)
    print(f"\n✅ Done. Output written to {OUTPUT}")

if __name__ == "__main__":
    main()
