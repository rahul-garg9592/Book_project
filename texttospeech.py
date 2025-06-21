# Filename: edge_tts_converter.py

import os
import asyncio
import edge_tts

SUMMARY_DIR = "summaries"
AUDIO_DIR = "audio_summaries"
VOICE = "en-US-JennyNeural"  # You can try other voices like "en-GB-RyanNeural", etc.

async def convert_file_to_audio(file_path, audio_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        if not text.strip():
            print(f"⚠️ Skipping empty file: {file_path}")
            return

    print(f"🎙️ Converting {os.path.basename(file_path)} to audio...")
    communicate = edge_tts.Communicate(text, voice=VOICE)
    await communicate.save(audio_path)
    print(f"✅ Audio saved: {audio_path}")

def convert_summaries_to_audio():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    txt_files = [f for f in os.listdir(SUMMARY_DIR) if f.endswith(".txt")]

    tasks = []
    for file in txt_files:
        txt_path = os.path.join(SUMMARY_DIR, file)
        mp3_name = file.replace(".txt", ".mp3")
        mp3_path = os.path.join(AUDIO_DIR, mp3_name)
        tasks.append(convert_file_to_audio(txt_path, mp3_path))

    asyncio.run(run_all(tasks))

async def run_all(tasks):
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    convert_summaries_to_audio()
