import sounddevice as sd
import numpy as np
import speech_recognition as sr
import io
import os
import subprocess
import time
import winsound
from scipy.io.wavfile import write

# --- KONFIGURATION (STABILITÄTS-MODUS v17) ---
MIC_ID = 1
FS = 44100  
START_WORDS = ["hey ji", "hey gee", "hey g", "hi gee", "hallo gee", "starten", "system an"]
# "aus" entfernt! Nur noch Phrasen für maximale Sicherheit
STOP_WORDS = ["gute nacht", "nexus aus", "licht aus", "feierabend", "system aus", "schlafen gehen"]
BASE_PATH = r"C:\Users\René\Desktop\LM Projekte"

def execute_batch(batch_file):
    try:
        target = os.path.join(BASE_PATH, batch_file)
        subprocess.Popen(f'start "" "{batch_file}"', shell=True, cwd=BASE_PATH)
    except: pass

r = sr.Recognizer()

def listen_loop():
    print(f"[EAR] Fokus auf ID {MIC_ID}. Warte auf Resonanz...")
    while True:
        try:
            with sd.InputStream(device=MIC_ID, channels=1, samplerate=FS, dtype='int16') as stream:
                recording, overflow = stream.read(int(3 * FS))
            
            byte_io = io.BytesIO()
            write(byte_io, FS, recording)
            byte_io.seek(0)
            
            with sr.AudioFile(byte_io) as source:
                audio_data = r.record(source)
                try:
                    command = r.recognize_google(audio_data, language="de-DE").lower()
                    print(f"\n[VOICE] Erkannt: '{command}'")
                    
                    # --- LICHT ---
                    if any(word in command for word in START_WORDS):
                        winsound.Beep(1000, 400)
                        execute_batch("01_ALL_SYSTEMS_GO.bat")
                        time.sleep(15) # Kurze Verschnaufpause
                        winsound.Beep(600, 100); winsound.Beep(900, 100)

                    # --- SCHATTEN ---
                    elif any(word in command for word in STOP_WORDS):
                        winsound.Beep(500, 600)
                        execute_batch("02_NEXUS_SHUTDOWN.bat")
                        time.sleep(15) 
                        winsound.Beep(600, 100); winsound.Beep(900, 100)
                except: pass 
        except:
            time.sleep(2)

if __name__ == "__main__":
    winsound.Beep(800, 200)
    listen_loop()




