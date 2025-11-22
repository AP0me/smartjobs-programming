import json
import os

# --- CONFIGURATION ---
INPUT_FILE = 'categorized_technologies.json'
OUTPUT_FILE = 'categorized_technologies_merged.json'

# Mapping Rules: "Source Bucket" -> "Target Bucket"
# The script moves contents from Source to Target and removes Source.
MERGE_MAPPING = {
    "Laravel": "PHP",
    ".NET": "C#",
    "Spring": "Java",
    "Flutter": "Dart",
    "Golang": "Go",
    "Django": "Python",
    "TypeScript": "JavaScript"
}

def merge_buckets():
    # 1. Load Data
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return

    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON.")
        return

    print(f"Loaded {len(data)} categories. Starting merge operation...\n")

    # 2. Perform Merge (OR Operation)
    for source, target in MERGE_MAPPING.items():
        # Only proceed if the source bucket (e.g., Laravel) actually exists in the file
        if source in data:
            source_urls = set(data[source])
            
            # Ensure target bucket (e.g., PHP) exists; if not, create it
            if target not in data:
                data[target] = []
            
            target_urls = set(data[target])
            
            # THE OR OPERATION (Set Union)
            # Combines both sets and removes duplicates
            merged_set = target_urls | source_urls
            
            # Update the target bucket with the merged result
            data[target] = list(merged_set)
            
            # Remove the old source bucket
            del data[source]
            
            print(f"MERGED: '{source}' ({len(source_urls)} items) -> '{target}'")
            print(f"        New '{target}' count: {len(data[target])}")
        else:
            # Optional: Print if source wasn't found (useful for debugging scraper list)
            # print(f"Skipped: '{source}' not found in data.")
            pass

    # 3. Save Results
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

    print(f"\nMerge complete. Saved to '{OUTPUT_FILE}'.")
    print(f"Total categories remaining: {len(data)}")

if __name__ == "__main__":
    merge_buckets()