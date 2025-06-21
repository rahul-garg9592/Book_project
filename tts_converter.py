import os
from elevenlabs import generate, save, set_api_key

# Your ElevenLabs API key
set_api_key("sk_5109b59752d0abd93d8c6927b747d316cbe3d58f231ef105")

# Optional: use a voice name from your ElevenLabs dashboard
VOICE = "Rachel"

def convert_text_to_audio(summary_dir="summaries", audio_dir="audio_summaries"):
    os.makedirs(audio_dir, exist_ok=True)

    for filename in os.listdir(summary_dir):
        if filename.endswith("_summary.txt"):
            text_path = os.path.join(summary_dir, filename)

            with open(text_path, "r", encoding="utf-8") as f:
                text = f.read()

            if len(text) < 20:
                print(f"⚠️ Skipping empty/short file: {filename}")
                continue

            print(f"🎤 Converting {filename} to audio using ElevenLabs...")

            try:
                audio = generate(text=text, voice=VOICE, model="eleven_multilingual_v2")
                output_file = os.path.join(audio_dir, filename.replace(".txt", ".mp3"))
                save(audio, output_file)
                print(f"✅ Saved audio to {output_file}")
            except Exception as e:
                print(f"❌ Failed to convert {filename}: {e}")

if __name__ == "__main__":
    convert_text_to_audio()
