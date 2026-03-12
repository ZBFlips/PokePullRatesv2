import json
import os
import time
import urllib.request
import urllib.parse
from urllib.error import HTTPError

# Configuration
API_URL = "https://archives.bulbagarden.net/w/api.php"
OUTPUT_DIR = "pack_art"

HEADERS = {
    "User-Agent": "PullRatesDataBot/1.0 (Data collection for TCG pull rates project)"
}

def fetch_json(url):
    time.sleep(2) # Strict rate limiting
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason} for {url}")
        return {}
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return {}

def download_image(url, filepath):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    files = []
    print("Executing brute-force keyword search across the media database...")
    
    # 1. Search for all files with "booster pack" in the title or description
    sroffset = 0
    
    while True:
        query_params = {
            "action": "query",
            "list": "search",
            "srsearch": "booster pack",
            "srnamespace": "6", # 6 is the File namespace in MediaWiki
            "srlimit": "500",
            "format": "json"
        }
        if sroffset > 0:
            query_params["sroffset"] = sroffset
            
        encoded_params = urllib.parse.urlencode(query_params)
        url = f"{API_URL}?{encoded_params}"
        
        data = fetch_json(url)
        if "query" in data and "search" in data["query"]:
            for item in data["query"]["search"]:
                title = item["title"]
                if title not in files:
                    files.append(title)
                
        if "continue" in data and "sroffset" in data["continue"]:
            sroffset = data["continue"]["sroffset"]
        else:
            break

    print(f"Found {len(files)} potential pack images. Beginning download...")

    # 2. Fetch the direct image URL for each file and download
    for title in files:
        query_params = {
            "action": "query",
            "titles": title,
            "prop": "imageinfo",
            "iiprop": "url",
            "format": "json"
        }
        encoded_params = urllib.parse.urlencode(query_params)
        url = f"{API_URL}?{encoded_params}"
        
        data = fetch_json(url)
        pages = data.get("query", {}).get("pages", {})
        
        for page_id, page_data in pages.items():
            if "imageinfo" in page_data:
                img_url = page_data["imageinfo"][0]["url"]
                
                filename = title.replace("File:", "").replace(" ", "_")
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                if not os.path.exists(filepath):
                    if download_image(img_url, filepath):
                        print(f"Downloaded: {filename}")
                    time.sleep(1) # Strict rate limiting to prevent IP ban
                else:
                    print(f"Skipped (exists): {filename}")

if __name__ == "__main__":
    main()