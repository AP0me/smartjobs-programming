import json
import os

# --- CONFIGURATION ---
INPUT_FILE = 'categorized_technologies_merged.json'
OUTPUT_FILE = 'technology_counts.json'

def count_categories():
    # 1. Check if input file exists
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file '{INPUT_FILE}' not found.")
        print("Please run the categorization script first.")
        return

    # 2. Load the data
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{INPUT_FILE}'.")
        return

    # 3. Calculate Counts
    # Structure is { "Language": ["url1", "url2"] }
    # We want { "Language": count }
    stats = {}
    total_mentions = 0
    
    for category, urls in data.items():
        count = len(urls)
        stats[category] = count
        total_mentions += count

    # 4. Sort data by count (Highest to Lowest) for better readability
    sorted_stats = dict(sorted(stats.items(), key=lambda item: item[1], reverse=True))

    # 5. Print Report to Console
    print("-" * 40)
    print(f"{'TECHNOLOGY':<20} | {'COUNT':<10}")
    print("-" * 40)
    
    for tech, count in sorted_stats.items():
        print(f"{tech:<20} | {count:<10}")
    
    print("-" * 40)
    print(f"{'TOTAL MENTIONS':<20} | {total_mentions:<10}")
    print("-" * 40)

    # 6. Save to JSON file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(sorted_stats, f, indent=4)

    print(f"\nSummary saved to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    count_categories()