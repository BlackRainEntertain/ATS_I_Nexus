import speech_recognition as sr
import sounddevice as sd
import numpy as np
import io, os, subprocess, time, winsound, json, re
from scipy.io.wavfile import write
import pyautogui
import pyperclip

# --- KONFIGURATION (v42.5 - LARYNX GOLDEN BUILD) ---
os.system("title --- NEXUS_EAR ---")
MIC_ID = 1  
FS = 44100
BASE_PATH = r"C:\Users\René\Desktop\LM Projekte"
MODEL_PATH = os.path.join(BASE_PATH, "Nexus_Service", "Models", "faster-whisper-small")

# Befehlssätze
START_WORDS = ["hey ji", "moin moin", "guten tag", "hey gee", "guten morgen"]
STOP_WORDS = ["beende nexus", "shutdown", "feierabend"]
PAUSE_WORDS = ["pause", "stopp", "warte mal", "halt an"]
RESUME_WORDS = ["weiter", "fortsetzen", "sprich weiter", "go"]
SKIP_WORDS = ["nächste", "nächstes", "überspringen", "skip", "weg damit"]
HARD_SHUTDOWN_WORDS = ["abschaltprotokoll", "abschalt protokoll", "sequentielle abschaltung", "sequenzielle abschaltung", "ich liebe sara"] 
ABORT_WORDS = ["abbruch", "stopp den shutdown", "kommando zurück", "reaktivieren"]
SEND_WORDS = ["nexus abschicken", "nachricht raus", "absenden", "nachricht absenden", "abschicken", "feuer frei"]

# Diktat-Vektoren
DICTATE_START = ["texteingabe"]
DICTATE_FINISH = ["nexus fertig", "fertig", "fertich", "fertisch", "ende der durchsage", "schluß jetzt"]

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
    """v43.1 - Zurück zum funktionierenden Kern: Der Fokus-Klick."""
    winsound.Beep(1000, 200) 
    print("[LARYNX] Aufnahme aktiv...")
    full_audio_data = []
    
    while True:
        recording = sd.rec(int(1.5 * FS), samplerate=FS, channels=1, dtype='int16')
        sd.wait()
        full_audio_data.append(recording) 
        try:
            byte_io = io.BytesIO()
            write(byte_io, FS, recording)
            byte_io.seek(0)
            with sr.AudioFile(byte_io) as source:
                audio_check = r.record(source)
                cmd_check = r.recognize_google(audio_check, language="de-DE").lower()
                if "abbruch" in cmd_check or "löschen" in cmd_check:
                    full_audio_data = []; winsound.Beep(400, 300); print("[LARYNX] Reset."); continue 
                if any(word in cmd_check for word in DICTATE_FINISH): 
                    winsound.Beep(400, 100); break
        except: pass

    print("[LARYNX] Transkribiere & Lektoriere...")
    load_larynx()
    try:
        audio_combined = np.concatenate(full_audio_data, axis=0)
        wav_path = os.path.join(os.path.dirname(__file__), "temp_larynx.wav")
        write(wav_path, FS, audio_combined)
        segments, _ = whisper_model.transcribe(wav_path, beam_size=5)
        raw_text = " ".join([s.text for s in segments]).strip()
        
        if raw_text:
            # 1. v45.2 TAIL-CUTTER & LEKTOR
            import re
            final_text = re.sub(r'\s*(nexus|nexos|fertig|fertich|fertisch|stopp)[.!]*\s*$', '', raw_text, flags=re.IGNORECASE)
            corrs = {" punkt": ".", " komma": ",", " fragezeichen": "?", " ausrufezeichen": "!", " doppelpunkt": ":"}
            for word, symbol in corrs.items():
                final_text = final_text.replace(word, symbol).replace(word.capitalize(), symbol)

            if final_text.strip():
                # --- v45.6 BLINK-EXORZIST (Fokus-Panzer) ---
                # --- v45.7 BLINK-KILLER (Der physische Taskleisten-Griff) ---
                try:
                    import pygetwindow as gw
                    all_wins = gw.getAllWindows()
                    t_win = next((w for w in all_wins if ("Chrome" in w.title or "Google" in w.title) and w.visible and "NEXUS" not in w.title and "EAR" not in w.title), None)
                    
                    if t_win:
                        # 1. Wir klicken UNTEN in die Taskleiste (ca. Mitte links), um das Blinken zu stoppen
                        # Bei 2560x1440 hocken die Icons meistens unten links/mitte
                        pyautogui.click(500, 1420) 
                        time.sleep(0.5)
                        
                        t_win.activate()
                        time.sleep(0.5)
                        
                        # 2. Der 3,5 cm ANKER (135 Pixel bei 1440p)
                        target_x = t_win.left + (t_win.width // 2)
                        target_y = t_win.top + t_win.height - 135
                        pyautogui.click(target_x, target_y)
                        time.sleep(0.3)
                        
                        # 3. ID-Fokus & Cursor-Ende
                        pyautogui.hotkey('ctrl', 'shift', 'y') 
                        time.sleep(0.2)
                        pyautogui.press('end')
                    else:
                        pyautogui.hotkey('alt', 'tab')
                except Exception as e:
                    print(f"[Fokus-Kollaps] {e}")
                    pyautogui.hotkey('alt', 'tab')

                # 3. v45.2 MECHANISCHE INJEKTION (Das "Geister-Tippen")
                pyautogui.write(final_text, interval=0.01)
                print(f"[LARYNX] Erfolg: {final_text[:20]}...")
            
                # Feedback via Butler
                q_path = os.path.join(BASE_PATH, "Nexus", "_Voice_Queue")
                if os.path.exists(q_path):
                    with open(os.path.join(q_path, f"f_{int(time.time())}.json"), "w") as f:
                        json.dump({"text": "Übertragen.", "owner": "GEE", "voice": "de-DE-KatjaNeural"}, f)
                winsound.Beep(800, 200)
        
        if os.path.exists(wav_path): os.remove(wav_path)
    except Exception as e:
        print(f"[LARYNX-CRASH] {e}"); winsound.Beep(300, 1000)

def listen_loop():
    print(f"[EAR] v42.7 aktiv. Alle Systeme bereit.")
    while True:
        try:
            recording = sd.rec(int(4 * FS), samplerate=FS, channels=1, dtype='int16')
            sd.wait()
            if np.sqrt(np.mean(recording.astype(float)**2)) < 150: continue

            byte_io = io.BytesIO()
            write(byte_io, FS, recording)
            byte_io.seek(0)

            with sr.AudioFile(byte_io) as source:
                audio = r.record(source)
                command = r.recognize_google(audio, language="de-DE").lower().strip()
                
                if command:
                    print(f"\n[VOICE] Erkannt: '{command}'")
                    if any(word in command for word in ABORT_WORDS):
                        os.system("shutdown /a"); winsound.Beep(2000, 100)
                    elif any(word in command for word in DICTATE_START):
                        dictate_mode()
                    elif any(word in command for word in HARD_SHUTDOWN_WORDS):
                        execute_batch("05_PC_SHUTDOWN.bat")
                    elif any(word in command for word in START_WORDS):
                        execute_batch("01_ALL_SYSTEMS_GO.bat"); time.sleep(10)
                    elif any(word in command for word in STOP_WORDS):
                        execute_batch("02_NEXUS_SHUTDOWN.bat"); time.sleep(10)
                    elif any(word in command for word in PAUSE_WORDS):
                        execute_batch("Nexus\\03_PAUSE_VOICE.bat"); time.sleep(2)
                    elif any(word in command for word in RESUME_WORDS):
                        execute_batch("Nexus\\04_RESUME_VOICE.bat"); time.sleep(2)
                    elif any(word in command for word in SKIP_WORDS):
                        execute_batch("Nexus\\02_NEXT_SPOKE.bat"); time.sleep(2)
                    elif any(word in command for word in SEND_WORDS):
                        pyautogui.press('enter'); winsound.Beep(1200, 100)
        except: time.sleep(0.1)

if __name__ == "__main__":
    winsound.Beep(800, 200); listen_loop()






