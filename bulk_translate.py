import os
import json
import asyncio
import sys
from app.translation_service import translate_content

# Fix encoding for Windows terminal
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SOURCE_DIR = r"c:\Users\Admin\Downloads\content\content"
TARGET_LANGS = ["ta", "te", "mr", "kn", "gu", "bn"]

def extract_pairs(data, pairs):
    """Recursively extract strings that look like titles or descriptions."""
    if isinstance(data, dict):
        # Look for common key pairs
        title = None
        desc = None
        
        # Priority keys
        title_keys = ["title", "titleHindi", "heroTitle", "sectionTitle", "label"]
        desc_keys = ["description", "descriptionHi", "descriptionHindi", "sectionDesc", "heroDesc", "subtitle"]
        
        for k, v in data.items():
            if k in title_keys and isinstance(v, str) and len(v.strip()) > 0:
                title = v.strip()
            if k in desc_keys and isinstance(v, str) and len(v.strip()) > 0:
                desc = v.strip()
        
        if title and desc:
            pairs.append({"title": title, "description": desc})
        elif title:
            # If only title exists, we still want it
            pairs.append({"title": title, "description": ""})
        elif desc:
            # If only desc exists
            pairs.append({"title": "", "description": desc})
            
        # Continue recursion
        for v in data.values():
            extract_pairs(v, pairs)
            
    elif isinstance(data, list):
        for item in data:
            extract_pairs(item, pairs)

async def main():
    all_pairs = []
    
    print("Step 1: Aggregating content from JSON files...")
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if file == "hi.json":
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        extract_pairs(data, all_pairs)
                except Exception as e:
                    print(f"Error reading {path}: {e}")

    # Deduplicate based on title and description
    unique_pairs = []
    seen = set()
    for p in all_pairs:
        key = (p["title"], p["description"])
        if key not in seen and (p["title"] or p["description"]):
            unique_pairs.append(p)
            seen.add(key)

    print(f"Found {len(unique_pairs)} unique content blocks.")
    
    # Results containers
    final_outputs = {lang: {} for lang in TARGET_LANGS}
    
    print(f"Step 2: Translating into {len(TARGET_LANGS)} languages...")
    
    # We will process sequentially to avoid hitting rate limits too hard, 
    # but we could use asyncio.gather with a semaphore if needed.
    count = 0
    total = len(unique_pairs)
    
    for idx, pair in enumerate(unique_pairs, start=1):
        content_id = idx
        title_hi = pair["title"]
        desc_hi = pair["description"]
        
        print(f"[{idx}/{total}] Processing content_id: {content_id}")
        
        for lang in TARGET_LANGS:
            try:
                # Using the existing service which handles caching (json_store)
                record = await translate_content(content_id, title_hi, desc_hi, lang)
                
                # Format for the specific requested output:
                # { "ID": { "content_id": ID, "language_code": "lang", ... } }
                final_outputs[lang][str(content_id)] = {
                    "content_id": content_id,
                    "language_code": lang,
                    "translated_title": record["translated_title"],
                    "translated_description": record["translated_description"]
                }
            except Exception as e:
                print(f"  Error translating {content_id} to {lang}: {e}")

    print("Step 3: Writing output files...")
    for lang in TARGET_LANGS:
        filename = f"{lang}.json"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(final_outputs[lang], f, ensure_ascii=False, indent=2)
            print(f"  Created {filename}")
        except Exception as e:
            print(f"  Error writing {filename}: {e}")

    print("Bulk translation complete.")

if __name__ == "__main__":
    asyncio.run(main())
