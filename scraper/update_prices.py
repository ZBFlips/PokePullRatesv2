#!/usr/bin/env python3
"""
PullRates.gg — Automated Price Updater
Scrapes ThePriceDex for card prices and PriceCharting for sealed packs.
"""

import json
import re
import time
import sys
import random
import http.cookiejar
import gzip
import io
import urllib.request
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

# ── Config ────────────────────────────────────────────────────
BASE_URL    = "https://www.thepricedex.com"
OUTPUT      = "prices.json"
DELAY       = 3.0
MAX_RETRIES = 3
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br", # Tells the server you can handle compressed data
    "Referer": "https://www.google.com/",
    "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Upgrade-Insecure-Requests": "1"
}

# ── Set definitions ───────────────────────────────────────────
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

RARITY_MAP = {
    "mega hyper rare": "MHR", "hyper rare": "HR", "special illustration rare": "SIR",
    "mega attack rare": "MAR", "illustration rare": "IR", "ace spec rare": "ACE",
    "double rare": "DR", "shiny rare": "SHR", "shiny ultra rare": "SHU",
    "tg secret rare": "TGS", "rainbow rare": "RBOW", "tg ultra rare": "TGU",
    "tg rare holo vmax": "TGVM", "tg rare holo v": "TGV", "tg rare holo": "TGH",
    "gg secret rare": "GGS", "gg ultra rare": "GGU", "gg rare holo vstar": "GGVS",
    "secret rare": "SR", "rare holo vstar": "VSTAR", "rare holo vmax": "VMAX",
    "rare holo v": "V", "radiant rare": "RAD", "rare holo": "RH",
    "ultra rare": "UR", "rare": "R", "uncommon": "U", "common": "C"
}

# ── Classes & Helpers ─────────────────────────────────────────

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tokens = []
    def handle_data(self, data):
        text = data.strip()
        if text: self.tokens.append(text)

def parse_price(text):
    if not text: return None
    cleaned = re.sub(r"[^\d.]", "", str(text).replace(",", ""))
    try:
        return round(float(cleaned), 2)
    except: return None

def fetch(url, retries=MAX_RETRIES):
    for attempt in range(retries):
        try:
            req = Request(url, headers=HEADERS)
            with urlopen(req, timeout=25) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except:
            time.sleep(DELAY)
    return None

# ── Core Scrapers ─────────────────────────────────────────────

def fetch(url, retries=MAX_RETRIES):
    for attempt in range(retries):
        try:
            req = Request(url, headers=HEADERS)
            with opener.open(req, timeout=25) as resp:
                data = resp.read()
                # Handle Gzip if the server sends it (very common for Cloudflare)
                if resp.info().get('Content-Encoding') == 'gzip':
                    data = gzip.decompress(data)
                return data.decode("utf-8", errors="replace")
        except HTTPError as e:
            if e.code == 403:
                print(f"    × Blocked (403) on {url}. Trying longer wait...")
                time.sleep(15)
            elif e.code == 429:
                print(f"    × Rate Limited (429). Sleeping 30s...")
                time.sleep(30)
        except Exception as e:
            time.sleep(DELAY)
    return None

def fetch_sealed_pack_price(set_slug):
    url = f"https://www.pricecharting.com/game/pokemon-{set_slug}/{set_slug}-booster-pack"
    html = fetch(url)
    if not html: return None
    match = re.search(r'id="used_price"[^>]*>\s*\$?([\d,]+\.?\d*)', html, re.I)
    return parse_price(match.group(1)) if match else None
    

def parse_pull_rates_page(html):
    if not html: return {}, None
    pack_ev = None
    ev_m = re.search(r'Booster Pack EV.*?\$([\d,]+\.?\d*)', html, re.I | re.S)
    if ev_m: pack_ev = parse_price(ev_m.group(1))

    parser = TextExtractor()
    parser.feed(html)
    tokens = parser.tokens
    rarity_prices = {}
    
    for i, token in enumerate(tokens):
        key = RARITY_MAP.get(token.lower())
        if key:
            for j in range(i + 1, min(i + 15, len(tokens))):
                if '$' in tokens[j]:
                    price = parse_price(tokens[j])
                    ev = parse_price(tokens[j+1]) if (j+1 < len(tokens)) else 0
                    rarity_prices[key] = {"avgPrice": price, "ev": ev or 0}
                    break
    return rarity_prices, pack_ev

def parse_guide_page(html):
    if not html: return {}
    # Extract names from H2 and prices from H5
    names = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.I | re.S)
    prices = re.findall(r'<h5[^>]*>(.*?)</h5>', html, re.I | re.S)
    data = {}
    for n, p in zip(names, prices):
        clean_name = re.sub(r'#\S.*$', '', n).strip().lower()
        price_val = parse_price(p)
        if price_val: data[clean_name] = price_val
    return data

# ── Main ──────────────────────────────────────────────────────

def main():
    try:
        with open(OUTPUT) as f: existing = json.load(f)
    except: existing = {"sets": {}}

    now = datetime.now(timezone.utc)
    new_data = {
        "lastUpdated": f"{now.strftime('%B')} {now.day}, {now.year}",
        "sets": {}
    }

    for s in SETS:
        sid, slug = s["id"], s["slug"]
        print(f"Scraping {slug}...")

        time.sleep(random.uniform(3.0, 7.0))
        
        p_html = fetch(f"{BASE_URL}/set/{sid}/{slug}/pull-rates")
        rarity_prices, pack_ev = parse_pull_rates_page(p_html)
        
        g_html = fetch(f"{BASE_URL}/guides/most-expensive-{s['guide']}-cards")
        top_prices = parse_guide_page(g_html)
        
        sealed_price = fetch_sealed_pack_price(slug)
        
        ex = existing.get("sets", {}).get(sid, {})
        if not rarity_prices: rarity_prices = ex.get("rarities", {})
        if not pack_ev: pack_ev = ex.get("packEV", 0)
        if not sealed_price: sealed_price = ex.get("packResalePrice", 0)

        top_card = ex.get("topCard", {"name": "N/A", "price": 0})
        if top_prices:
            best_name = max(top_prices, key=top_prices.get)
            top_card = {"name": best_name.title(), "price": top_prices[best_name]}

        new_data["sets"][sid] = {
            "rarities": rarity_prices,
            "packEV": pack_ev,
            "packResalePrice": sealed_price,
            "topCard": top_card,
            "notablePrices": top_prices
        }
        time.sleep(DELAY)

    with open(OUTPUT, "w") as f:
        json.dump(new_data, f, indent=2)
    print("Update Complete.")

if __name__ == "__main__":
    main()
