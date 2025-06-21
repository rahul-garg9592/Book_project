import requests
import re
import os
from bs4 import BeautifulSoup

def fetch_all_book_ids():
    url = "https://www.gutenberg.org/browse/scores/top"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print("❌ Failed to fetch page:", e)
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    book_ids = set()
    for a_tag in soup.find_all("a", href=True):
        match = re.match(r"^/ebooks/(\d+)$", a_tag["href"])
        if match:
            book_ids.add(match.group(1))

    return sorted(book_ids)

def download_book(book_id, out_dir="downloaded_books"):
    url1 = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    url2 = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
    os.makedirs(out_dir, exist_ok=True)

    for url in [url1, url2]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            filename = os.path.join(out_dir, f"{book_id}.txt")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"✅ Downloaded book {book_id} → {filename}")
            return
        except Exception:
            continue

    print(f"❌ Failed to download book {book_id} from both URL formats.")

def main():
    book_ids = fetch_all_book_ids()
    print(f"📚 Found {len(book_ids)} books. Downloading first 168...")

    for book_id in book_ids[:168]:
        download_book(book_id)

if __name__ == "__main__":
    main()
