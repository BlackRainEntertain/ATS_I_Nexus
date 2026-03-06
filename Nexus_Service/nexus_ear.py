import speech_recognition as sr
import os
import subprocess
import time
import winsound

# --- KONFIGURATION (v19.2 - ACTIVE LISTENING) ---
MIC_ID = 1
START_WORDS = ["hey ji", "hey gee", "guten morgen", "system an"]
STOP_WORDS = ["gute nacht", "shutdown"]
BASE_PATH = r"C:\Users\René\Desktop\LM Projekte"

r = sr.Recognizer()
# --- DER TÜRSTEHER (Wichtig gegen Fernseher/Wind) ---
r.energy_threshold = 1000  # Erhöhe auf 1500, wenn der TV laut ist
r.dynamic_energy_threshold = False
r.pause_threshold = 0.8    # Wartet 0.8s Stille ab, bevor er den Satz abschliesst

def execute_batch(batch_file):
    try:
        full_path = os.path.join(BASE_PATH, batch_file)
        subprocess.Popen(f'start "" "{full_path}"', shell=True, cwd=BASE_PATH)
    except: pass

def listen_loop():
    with sr.Microphone(device_index=MIC_ID) as source:
        # GEHEIMWAFFE: Er misst 2 Sekunden die Stille in deinem Zimmer
        print(f"[EAR] Kalibriere Umgebungsgeräusche (2s Stille bitte)...")
        r.adjust_for_ambient_noise(source, duration=2)
        
        # Jetzt zeigt er dir an, welchen Schwellenwert er gewählt hat:
        print(f"[EAR] Ready! Dynamischer Schwellenwert: {r.energy_threshold}")
        
        # Wir erhöhen den Wert manuell um +10%, damit der TV nicht stört:
        r.energy_threshold += 100 
        
        while True:
            try:
                print(".", end="", flush=True) # Puls-Signal in der CMD
                audio = r.listen(source, timeout=None, phrase_time_limit=5)
                
                try:
                    command = r.recognize_google(audio, language="de-DE").lower().strip()
                    if command:
                        print(f"\n[VOICE] Erkannt: '{command}'")
                    
                    if any(word in command for word in START_WORDS):
                        winsound.Beep(1000, 400)
                        execute_batch("01_ALL_SYSTEMS_GO.bat")
                        time.sleep(15) 
                        winsound.Beep(600, 100); winsound.Beep(900, 100)

                    elif any(word in command for word in STOP_WORDS):
                        winsound.Beep(500, 600)
                        execute_batch("02_NEXUS_SHUTDOWN.bat")
                        time.sleep(15) 
                        winsound.Beep(600, 100); winsound.Beep(900, 100)
                        
                except sr.UnknownValueError: pass # Nichts erkannt
                except Exception as e: print(f"\nFehler: {e}")
                
            except Exception as e:
                print(f"\nTreiber/Timeout: {e}")
                time.sleep(1)

if __name__ == "__main__":
    winsound.Beep(800, 200)
    listen_loop()




