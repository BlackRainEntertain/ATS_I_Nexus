import speech_recognition as sr
import sounddevice as sd
import numpy as np
import io, os, subprocess, time, winsound, json, re
from scipy.io.wavfile import write
import pyautogui
import pyperclip
import sys

# --- KONFIGURATION (v42.8 - ARCHITECT STABILITY BUILD) ---
os.system("title --- NEXUS_EAR ---")
MIC_ID = 1  
FS = 48000
BASE_PATH = r"C:\Users\René\Desktop\LM Projekte"
MODEL_PATH = os.path.join(BASE_PATH, "Nexus_Service", "Models", "faster-whisper-small")

# Befehlssätze
START_WORDS = ["hey ji", "moin moin", "guten tag", "hey gee", "guten morgen"]
STOP_WORDS = ["beende nexus", "shutdown", "feierabend"]
PAUSE_WORDS = ["pause", "warte mal", "halt an"]
RESUME_WORDS = ["weiter", "fortsetzen", "sprich weiter"]
SKIP_WORDS = ["nächste", "nächstes", "überspringen", "skip", "weg damit"]
HARD_SHUTDOWN_WORDS = ["abschalt protokoll", "abschaltprotokoll", "sequentielle abschaltung", "sequenzielle abschaltung", "ich liebe sara", "ich liebe sarah"] 
ABORT_WORDS = ["abbruch", "stopp den shutdown", "kommando zurück", "reaktivieren"]
SEND_WORDS = ["nexus abschicken", "nachricht raus", "absenden", "nachricht absenden", "abschicken", "feuer frei"]

# Diktat-Vektoren
DICTATE_START = ["texteingabe"]
DICTATE_FINISH = ["nexus fertig", "fertig", "fertich", "fertisch", "ende der durchsage", "schluß jetzt", "nexosfertig"]

r = sr.Recognizer()
whisper_model = None

def load_larynx():
    global whisper_model
    if whisper_model is not None: return
    print("\n[LARYNX] Initialisiere CPU-Kern (Safe-Mode)...")
    try:
        from faster_whisper import WhisperModel
        whisper_model = WhisperModel(MODEL_PATH, device="cpu", compute_type="int8", local_files_only=True)
        winsound.Beep(1200, 200)
        print("[LARYNX] Kern bereit (CPU).")
    except Exception as e:
        print(f"[ERR] Kern-Fehler: {e}")
        winsound.Beep(300, 500)

def execute_batch(batch_file):
    try:
        subprocess.Popen(f'cmd /c start "" "{batch_file}"', shell=True, cwd=BASE_PATH)
    except: pass

def dictate_mode():
    pause_file = os.path.join(BASE_PATH, "Nexus", "NEXUS_PAUSE.tmp")
    with open(pause_file, "w") as f: f.write("Larynx_Active")
    winsound.Beep(1000, 200) 
    full_audio_data = []
    last_heartbeat = time.time()
    
    while True:
        if time.time() - last_heartbeat > 30:
            winsound.Beep(1400, 20) 
            last_heartbeat = time.time()

        recording = sd.rec(int(5.0 * FS), device=MIC_ID, samplerate=FS, channels=1, dtype='int16')
        sd.wait() 
        full_audio_data.append(recording)

        try:
            byte_io = io.BytesIO()
            write(byte_io, FS, recording)
            byte_io.seek(0)
            with sr.AudioFile(byte_io) as source:
                audio_check = r.record(source)
                cmd_check = r.recognize_google(audio_check, language="de-DE").lower()
                if any(word in cmd_check for word in ABORT_WORDS):
                    if os.path.exists(pause_file): os.remove(pause_file)
                    return 
                if any(word in cmd_check for word in DICTATE_FINISH):
                    break
        except: pass

    load_larynx()
    try:
        audio_combined = np.concatenate(full_audio_data, axis=0)
        wav_path = os.path.join(os.path.dirname(__file__), "temp_larynx.wav")
        write(wav_path, FS, audio_combined)
        
        segments, _ = whisper_model.transcribe(
            wav_path, beam_size=10, best_of=5,
            initial_prompt="Aria, Nyx, Nexus, Architekt, Butler, Larynx, Punkt, Komma, Hey Gee.", 
            vad_filter=True
        )

        final_text = " ".join([s.text for s in segments]).strip()
        if final_text:
            replacements = {" punkt": ".", " komma": ",", " neue zeile": "\n"}
            for word, symbol in replacements.items():
                final_text = final_text.replace(word, symbol)
            
            pyautogui.hotkey('ctrl', 'shift', 'y')
            time.sleep(0.4)
            pyautogui.write(final_text, interval=0.01)

            q_path = os.path.join(BASE_PATH, "Nexus", "_Voice_Queue")
            ticket_name = f"{int(time.time())}_Whisper_Fin.json"
            full_path = os.path.join(q_path, ticket_name)
            with open(full_path + ".tmp", "w", encoding="utf-8") as f:
                json.dump({"text": "Übertragen.", "owner": "GEE", "voice": "de-DE-KatjaNeural"}, f, ensure_ascii=False)
            os.rename(full_path + ".tmp", full_path)
    except Exception as e:
        print(f"[LARYNX-CRASH] {e}")
    finally:
        if os.path.exists(pause_file): os.remove(pause_file)
        winsound.Beep(800, 200)

def listen_loop():
    print(f"[EAR] v42.8 aktiv. Dauerbetrieb ohne Sleep-Timer (Stabilitäts-Fix).")
    while True:
        try:
            recording = sd.rec(int(4 * FS), device=MIC_ID, samplerate=FS, channels=1, dtype='int16')
            sd.wait()
            
            if np.sqrt(np.mean(recording.astype(float)**2)) < 150: 
                continue

            byte_io = io.BytesIO()
            write(byte_io, FS, recording)
            byte_io.seek(0)

            with sr.AudioFile(byte_io) as source:
                audio = r.record(source)
                command = r.recognize_google(audio, language="de-DE").lower().strip()
                
                if command:
                    print(f"\n[VOICE] Erkannt: '{command}'")
                    
                    # 1. Abbruch-Check (Falls man es sich anders überlegt)
                    if any(word in command for word in ABORT_WORDS):
                        os.system("shutdown /a"); winsound.Beep(2000, 100)
                    
                    # 2. DAS HERUNTERFAHREN (Triggert deine S304_PC_SHUTDOWN.bat)
                    elif any(word in command for word in HARD_SHUTDOWN_WORDS):
                        print("[!] S304_PC_SHUTDOWN wird ausgeführt...")
                        execute_batch("S304_PC_SHUTDOWN.bat")
                        time.sleep(5)

                    # 3. Restliche Befehle
                    elif any(word in command for word in DICTATE_START):
                        dictate_mode()
                    elif any(word in command for word in START_WORDS):
                        execute_batch("S601_ALL_SYSTEMS_GO.bat"); time.sleep(10)
                    elif any(word in command for word in STOP_WORDS):
                        execute_batch("S502_NEXUS_SHUTDOWN.bat"); time.sleep(10)
                    elif any(word in command for word in PAUSE_WORDS):
                        execute_batch("Nexus\\03_PAUSE_VOICE.bat"); time.sleep(2)
                    elif any(word in command for word in RESUME_WORDS):
                        execute_batch("Nexus\\04_RESUME_VOICE.bat"); time.sleep(2)
                    elif any(word in command for word in SKIP_WORDS):
                        execute_batch("Nexus\\02_NEXT_SPOKE.bat"); time.sleep(2)
                    elif any(word in command for word in SEND_WORDS):
                        pyautogui.press('enter'); winsound.Beep(1200, 100)
        except:
            time.sleep(0.1)

if __name__ == "__main__":
    winsound.Beep(800, 200); listen_loop()
