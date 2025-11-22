import json
import time
import requests
import re
from collections import defaultdict

from bs4 import BeautifulSoup

# --- CONFIGURATION (Stage 1: Initial Filter) ---
INPUT_FILE = 'hrefs.json'
OUTPUT_FILE_STAGE_1 = 'filtered_results.json' # Renamed for clarity
TARGET_CATEGORY = "Development"
ELEMENT_SELECTOR_CATEGORY = ".job-detail-des .tag-item" # Element for 'Development' category check

# --- CONFIGURATION (Stage 2: Tech Categorization) ---
INPUT_FILE_STAGE_2 = OUTPUT_FILE_STAGE_1
OUTPUT_FILE_STAGE_2 = 'categorized_technologies.json' # New final output file
# Selector for the 4th <li> element (index 3) inside .job-detail-des
TECH_SELECTOR = ".job-detail-des>li:nth-child(4)"
# Keywords to search for and their corresponding 'buckets'
TECH_KEYWORDS = {
    "PHP": "backend_dev",
    "Laravel": "backend_dev",
    "C#": "backend_dev",
    ".NET": "backend_dev",
    "Java": "backend_dev",
    "Spring": "backend_dev",
    "Dart": "mobile_dev",
    "Go": "mobile_dev",
    "Golang": "mobile_dev",
    "Kotlin": "mobile_dev",
    "Swift": "mobile_dev",
    "Flutter": "mobile_dev",
    "Python": "data_science_or_backend",
    "Django": "data_science_or_backend",
    "SQL": "database",
    "JavaScript": "frontend_dev",
    "TypeScript": "frontend_dev",
}
# Headers and sleep time remain the same
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
SLEEP_TIME = 0.1

# --- STAGE 2: Categorize Technologies ---
def categorize_technologies():
    """Loads filtered URLs, scrapes a new element, and categorizes keywords into buckets (languages)."""
    # Load the results from Stage 1
    try:
        with open(INPUT_FILE_STAGE_2, 'r', encoding='utf-8') as f:
            # We only care about the keys (URLs) for the next step
            filtered_urls = list(json.load(f).keys())
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE_STAGE_2} not found. Run Stage 1 first.")
        return
    
    if not filtered_urls:
        print("No URLs found in the filtered results file. Exiting Stage 2.")
        return

    # Initialize the structure for the final output
    # defaultdict ensures that when we access a key (bucket), if it doesn't exist, it creates an empty list
    final_categorized_data = defaultdict(list)
    
    print(f"\nStarting STAGE 2: Categorize technologies for {len(filtered_urls)} URLs...")
    
    # Iterate through the URLs from the first stage's output
    for url in filtered_urls:
        try:
            print(f"Categorizing: {url}")
            response = requests.get(url, headers=HEADERS, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Use the new selector for the 4th <li> element
                element = soup.select_one(TECH_SELECTOR)
                
                if element:
                    # Get the text content and convert to lowercase for case-insensitive search
                    text_content = element.get_text().lower()
                    found_keywords = []

                    # Check for each keyword
                    for keyword, bucket in TECH_KEYWORDS.items():
                        # Use keyword.lower() to ensure case-insensitivity
                        if keyword.lower()+'\n' in text_content:
                            final_categorized_data[keyword].append(url)
                            found_keywords.append(keyword)
                            
                    if found_keywords:
                        print(f"  -> Found keywords: {', '.join(found_keywords)}")
                    else:
                        print("  -> No target keywords found in the element." + text_content)

                else:
                    print("  -> Tech element not found on page with selector.")
            else:
                print(f"  -> Failed to retrieve (Status: {response.status_code})")

            time.sleep(SLEEP_TIME)

        except Exception as e:
            print(f"  -> Error processing {url}: {e}")

    # Convert defaultdict back to a regular dict for JSON output
    output_data = dict(final_categorized_data) 

    # Save Stage 2 results, overwriting the file each time as requested
    with open(OUTPUT_FILE_STAGE_2, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4)

    print(f"\nSTAGE 2 Complete. Results saved to {OUTPUT_FILE_STAGE_2}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    categorize_technologies()