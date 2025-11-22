import json
import time
import requests
import re

from bs4 import BeautifulSoup

# --- CONFIGURATION ---
INPUT_FILE = 'hrefs.json'
OUTPUT_FILE = 'filtered_results.json'
TARGET_CATEGORY = "Development"
ELEMENT_SELECTOR = ".job-detail-des .tag-item" 

def scrape_and_filter():
    # 1. Load the list of URLs
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            url_list = json.load(f)
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found.")
        return

    # This dictionary will store the results
    # Structure: { "url": "found_text" }
    matching_data = {}

    # Headers act as a "disguise" so the website doesn't block the script immediately
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"Starting scrape of {len(url_list)} URLs...")

    # 2. Iterate through URLs
    for url in url_list:
        try:
            print(f"Checking: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            
            # Check if the request was successful (Status Code 200)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # 3. Find the specific element
                element = soup.select_one(ELEMENT_SELECTOR)
                
                if element:
                    text_content = element.get_text(strip=True)
                    
                    # 4. Check if text matches the category
                    # using .lower() for case-insensitive comparison
                    if re.search(TARGET_CATEGORY.lower(), text_content.lower()):
                        print(f"  -> Match found! ({text_content})")
                        matching_data[url] = text_content
                else:
                    print("  -> Element not found on page.")
            else:
                print(f"  -> Failed to retrieve (Status: {response.status_code})")

            # Be polite: Sleep for 1 second to avoid overwhelming the server
            time.sleep(0.1)

        except Exception as e:
            print(f"  -> Error processing {url}: {e}")

    # 5. Flush (save) results to output JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(matching_data, f, indent=4)

    print(f"\nScraping complete. {len(matching_data)} matches saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_and_filter()