import speech_recognition as sr
import sounddevice as sd
import numpy as np
import io, os, subprocess, time, winsound
from scipy.io.wavfile import write

# --- KONFIGURATION (v38.4 TOTAL-LOCKDOWN) ---
MIC_ID = 1  
FS = 44100
START_WORDS = ["hey ji", "moin moin", "lg", "guten tag", "hey gee", "guten morgen"]
STOP_WORDS = ["gute nacht", "shutdown", "feierabend"]
PAUSE_WORDS = ["pause", "stopp", "warte mal", "halt an"]
RESUME_WORDS = ["weiter", "fortsetzen", "sprich weiter", "go"]
SKIP_WORDS = ["nächste", "nächstes", "überspringen", "skip", "weg damit"]
HARD_SHUTDOWN_WORDS = ["abschaltprotokoll", "sequenzielle abschaltung", "ich liebe sara"] 

BASE_PATH = r"C:\Users\René\Desktop\LM Projekte"

r = sr.Recognizer()

def execute_batch(batch_file):
    try:
        subprocess.Popen(f'cmd /c start "" "{batch_file}"', shell=True, cwd=BASE_PATH)
    except:
        pass

def listen_loop():
    print(f"[EAR] v38.4 Resonanz aktiv (Lockdown-ready). Warte...")
    while True:
        try:
            recording = sd.rec(int(4 * FS), samplerate=FS, channels=1, dtype='int16')
            sd.wait()

            byte_io = io.BytesIO()
            write(byte_io, FS, recording)
            byte_io.seek(0)

            with sr.AudioFile(byte_io) as source:
                audio = r.record(source)
                command = r.recognize_google(audio, language="de-DE").lower().strip()
                if command:
                    print(f"\n[VOICE] Erkannt: '{command}'")
                    
                    if any(word in command for word in START_WORDS):
                        winsound.Beep(1000, 400); execute_batch("01_ALL_SYSTEMS_GO.bat"); time.sleep(15)
                    elif any(word in command for word in STOP_WORDS):
                        winsound.Beep(500, 600); execute_batch("02_NEXUS_SHUTDOWN.bat"); time.sleep(15)
                    elif any(word in command for word in PAUSE_WORDS):
                        winsound.Beep(600, 200); execute_batch("Nexus\\03_PAUSE_VOICE.bat"); time.sleep(5)
                    elif any(word in command for word in RESUME_WORDS):
                        winsound.Beep(900, 200); execute_batch("Nexus\\04_RESUME_VOICE.bat"); time.sleep(5)
                    elif any(word in command for word in SKIP_WORDS):
                        winsound.Beep(400, 300); execute_batch("Nexus\\02_NEXT_SPOKE.bat"); time.sleep(5)
                    # --- NEU: HARD PC SHUTDOWN ---
                    elif any(word in command for word in HARD_SHUTDOWN_WORDS):
                        winsound.Beep(300, 1000) # Langer tiefer Beep
                        execute_batch("05_PC_SHUTDOWN.bat")
                        time.sleep(20)

        except Exception as e:
            time.sleep(0.1)

if __name__ == "__main__":
    winsound.Beep(800, 200); listen_loop()



