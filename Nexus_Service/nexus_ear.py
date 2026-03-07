import speech_recognition as sr
import sounddevice as sd
import numpy as np
import io, os, subprocess, time, winsound
from scipy.io.wavfile import write

# --- KONFIGURATION (v38.1 TITAN-EAR) ---
MIC_ID = 1  # Dein Focusrite
FS = 44100
START_WORDS = ["hey ji", "moin moin", "lg", "guten tag", "hey gee", "guten morgen"]
STOP_WORDS = ["gute nacht", "shutdown", "feierabend"]
BASE_PATH = r"C:\Users\René\Desktop\LM Projekte"

r = sr.Recognizer()

def execute_batch(batch_file):
    try:
        subprocess.Popen(f'cmd /c start "" "{batch_file}"', shell=True, cwd=BASE_PATH)
    except: pass

def listen_loop():
    print(f"[EAR] v38.1 Resonanz aktiv (Pure Sounddevice). Warte...")
    while True:
        try:
            # 1. 4 Sekunden Audio-Snapshot (Kein PyAudio nötig!)
            recording = sd.rec(int(4 * FS), samplerate=FS, channels=1, dtype='int16')
            sd.wait()

            # 2. In den RAM schreiben für Google
            byte_io = io.BytesIO()
            write(byte_io, FS, recording)
            byte_io.seek(0)

            with sr.AudioFile(byte_io) as source:
                audio = r.record(source)
                command = r.recognize_google(audio, language="de-DE").lower().strip()
                if command:
                    print(f"\n[VOICE] Erkannt: '{command}'")
                    if any(word in command for word in START_WORDS):
                        winsound.Beep(1000, 400); execute_batch("01_ALL_SYSTEMS_GO.bat")
                        time.sleep(15)
                    elif any(word in command for word in STOP_WORDS):
                        winsound.Beep(500, 600); execute_batch("02_NEXUS_SHUTDOWN.bat")
                        time.sleep(15)
        except: pass

if __name__ == "__main__":
    winsound.Beep(800, 200); listen_loop()

