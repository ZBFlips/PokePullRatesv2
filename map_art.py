import os
import re
import shutil

# Configuration
INPUT_DIR = "pack_art"
OUTPUT_DIR = "images"
DATA_FILE = "data.js"

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"Directory '{INPUT_DIR}' not found. Run the scraper first.")
        return
        
    if not os.path.exists(DATA_FILE):
        print(f"File '{DATA_FILE}' not found in this directory.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Read your Javascript database
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 2. Extract every set ID and Name using Regex
    sets = []
    # Looks for the pattern: id: 'sv8', name: 'Surging Sparks'
    matches = re.finditer(r"id:\s*['\"]([^'\"]+)['\"].*?name:\s*['\"]([^'\"]+)['\"]", content, re.IGNORECASE | re.DOTALL)
    for match in matches:
        sets.append({"id": match.group(1), "name": match.group(2)})
        
    print(f"Extracted {len(sets)} sets directly from {DATA_FILE}.")
    
    files = os.listdir(INPUT_DIR)
    matched_sets = set()

    # 3. Fuzzy match the extracted names against the downloaded filenames
    for s in sets:
        set_id = s["id"]
        set_name = s["name"]
        
        # Strip special characters and split into words (e.g., "Scarlet & Violet" -> ["Scarlet", "Violet"])
        keywords = [k.lower() for k in re.split(r'[^a-zA-Z0-9]', set_name) if len(k) > 1]
        
        best_match = None
        max_score = 0
        
        for filename in files:
            # Calculate how many words from the set name appear in the file name
            score = sum(1 for kw in keywords if kw in filename.lower())
            
            # If we find a higher match score, set it as the new best match
            if score > max_score and score >= len(keywords) * 0.5: # Requires at least 50% keyword match
                max_score = score
                best_match = filename
                
        if best_match:
            new_filename = f"{set_id}.jpg"
            src_path = os.path.join(INPUT_DIR, best_match)
            dest_path = os.path.join(OUTPUT_DIR, new_filename)
            
            shutil.copy2(src_path, dest_path)
            print(f"Mapped: {set_name} -> {best_match}")
            matched_sets.add(set_id)
        else:
            print(f"⚠ No matching art found for: {set_name} ({set_id})")

    print(f"\nSuccessfully assigned {len(matched_sets)} out of {len(sets)} images.")

if __name__ == "__main__":
    main()