import os
import requests
import time

# ✅ Replace with your own key from https://openrouter.ai/keys
OPENROUTER_API_KEY = ""

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://yourproject.com",  # Optional but polite
    "X-Title": "Book Summary App"
}

MODEL = "mistralai/mistral-7b-instruct"  # Or try 'anthropic/claude-3-haiku' or 'openai/gpt-3.5-turbo'

def summarize_chunk(text_chunk):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an assistant that summarizes books in a clear and concise way."},
            {"role": "user", "content": f"Summarize the following part of a book:\n\n{text_chunk}"}
        ]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=HEADERS, json=payload)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Error during summarization:", e)
        return ""

def split_text_into_chunks(text, max_words=800):
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def summarize_book(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        full_text = f.read()

    chunks = split_text_into_chunks(full_text)
    print(f"📝 Summarizing {os.path.basename(file_path)} in {len(chunks)} chunks...")

    full_summary = ""
    for i, chunk in enumerate(chunks):
        print(f"🔹 Summarizing chunk {i+1}/{len(chunks)}...")
        summary = summarize_chunk(chunk)
        full_summary += summary.strip() + "\n\n"
        time.sleep(1)  # polite delay to avoid rate limit

    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(full_summary)
    print(f"✅ Summary saved to {output_path}")

def summarize_all_books(input_dir="downloaded_books", output_dir="summaries"):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace(".txt", "_summary.txt"))
            summarize_book(input_path, output_path)

if __name__ == "__main__":
    summarize_all_books()
