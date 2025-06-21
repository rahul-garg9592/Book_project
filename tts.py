from gtts import gTTS
import os

def convert_text_to_audio(summary_dir="summaries", audio_dir="audio_summaries"):
    os.makedirs(audio_dir, exist_ok=True)

    print(f"📂 Scanning directory: {summary_dir}")
    print(f"Files found: {os.listdir(summary_dir)}")

    for filename in os.listdir(summary_dir):
        if filename.endswith("_summary.txt"):  # <-- fix here
            text_path = os.path.join(summary_dir, filename)

            with open(text_path, "r", encoding="utf-8") as f:
                text = f.read()

            print(f"🎤 Converting {filename} to audio...")

            try:
                tts = gTTS(text=text, lang='en')
                audio_filename = filename.replace(".txt", ".mp3")
                audio_path = os.path.join(audio_dir, audio_filename)
                tts.save(audio_path)
                print(f"✅ Saved audio to: {audio_path}")
            except Exception as e:
                print(f"❌ Failed for {filename}: {e}")

# Run it
if __name__ == "__main__":
    convert_text_to_audio()
