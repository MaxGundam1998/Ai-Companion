import subprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PIPER = os.path.join(BASE_DIR, "piper", "piper")
VOICE = os.path.join(BASE_DIR, "voices", "en_GB-semaine-medium.onnx")
OUTPUT = os.path.join(BASE_DIR, "nikki_speech.wav")

def speak(text):
    if not text or not text.strip():
        return

    subprocess.run(
        [
            PIPER,
            "--model", VOICE,
            "--speaker", "3",
            "--output_file", OUTPUT
        ],
        input=text,
        text=True,
        check=True
    )

    subprocess.run(
        ["aplay", "-D", "plughw:2,0", OUTPUT],
        check=True
    )