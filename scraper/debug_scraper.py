import re
import urllib.request
from urllib.error import HTTPError

URL = "https://www.thepricedex.com/set/sv8/surging-sparks/pull-rates"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def main():
    print(f"Fetching {URL}...\n")
    try:
        req = urllib.request.Request(URL, headers=HEADERS)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
            # Check for Next.js JSON data (the holy grail of scraping)
            if '"props":{"pageProps"' in html or "__NEXT_DATA__" in html:
                print("✅ Found Next.js JSON data block! We can parse the raw JSON directly.")
            else:
                print("❌ No Next.js JSON block found. We must parse the DOM.")

            print("-" * 50)
            print("Searching for the Special Illustration Rare EV data block:\n")
            
            # Find where "Special Illustration Rare" is mentioned and print the surrounding 300 characters
            match = re.search(r'.{0,150}Special Illustration Rare.{0,150}', html, re.IGNORECASE)
            if match:
                print(match.group(0))
            else:
                print("Could not find 'Special Illustration Rare' in the HTML text.")
                
            print("-" * 50)
            
    except HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
   