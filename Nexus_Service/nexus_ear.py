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
    # 1. Butler-Pause-Signal setzen (Nutzt bestehende Infrastruktur)
    pause_file = os.path.join(BASE_PATH, "Nexus", "NEXUS_PAUSE.tmp")
    with open(pause_file, "w") as f: f.write("Larynx_Active")
    
    winsound.Beep(1000, 200) # Start-Signal
    full_audio_data = []
    last_heartbeat = time.time()
    
    while True:
        # 1. Beep-Check BEVOR die Aufnahme startet (Non-Blocking)
        if time.time() - last_heartbeat > 30:
            winsound.Beep(1400, 20) 
            last_heartbeat = time.time()

        # 2. Die 5.0-Sekunden Aufnahme
        recording = sd.rec(int(5.0 * FS), samplerate=FS, channels=1, dtype='int16')
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
                    # --- KATJA FEEDBACK ABBRUCH ---
                    q_path = os.path.join(BASE_PATH, "Nexus", "_Voice_Queue")
                    try:
                        with open(os.path.join(q_path, f"abt_{int(time.time())}.json"), "w", encoding="utf-8") as f:
                            json.dump({"text": "Abgebrochen.", "owner": "GEE", "voice": "de-DE-KatjaNeural"}, f)
                    except: pass
                    return 
                if any(word in cmd_check for word in DICTATE_FINISH):

                    break
        except: pass

    # 2. Lokale Transkription mit VAD (Filtert TV-Lärm)
    load_larynx()
    try:
        audio_combined = np.concatenate(full_audio_data, axis=0)
        wav_path = os.path.join(os.path.dirname(__file__), "temp_larynx.wav")
        write(wav_path, FS, audio_combined)
        
        # v47.0 - ISOLATION SHIELD (Finaler Schliff gegen TV-Kollision)
        segments, _ = whisper_model.transcribe(
            wav_path, 
            beam_size=10, 
            best_of=5,
            vad_filter=False, 
            vad_parameters=dict(
                threshold=0.45, 
                min_speech_duration_ms=250,
                min_silence_duration_ms=800
            ),
            initial_prompt="Aria, Realität, Fantasie, verschwammen, Leo.", 
            condition_on_previous_text=False
        )

        final_text = " ".join([s.text for s in segments]).strip()
        
        if final_text:
            # --- DER UNIVERSAL-FOKUS-MAGNET (v55) ---
            # Triggert den Tampermonkey-Fokus (Ctrl+Shift+Y) im aktiven Fenster
            pyautogui.hotkey('ctrl', 'shift', 'y')
            time.sleep(0.2) # Gedenksekunde für das UI-Fokus-Rendering
            
            # Jetzt wird getippt (Der Cursor sitzt dank Magnet schon in der Zeile)
            pyautogui.write(final_text, interval=0.01)
            # --- KATJA FEEDBACK (v50.0 - SAFE-WRITE SHIELD) ---
            q_path = os.path.join(BASE_PATH, "Nexus", "_Voice_Queue")
            try:
                ticket_name = f"{int(time.time())}_Whisper_Fin.json"
                full_path = os.path.join(q_path, ticket_name)
                # Wir schreiben erst die .tmp, damit der Butler keine halben Sachen kriegt
                with open(full_path + ".tmp", "w", encoding="utf-8") as f:
                    json.dump({"text": "Übertragen. Bereit zum Absenden.", "owner": "GEE", "voice": "de-DE-KatjaNeural"}, f, ensure_ascii=False)
                os.rename(full_path + ".tmp", full_path)
            except Exception as e:
                print(f"[ERR] Ticket-Schreibfehler: {e}")
            
            print("[LARYNX] Übertragung abgeschlossen.")
        else:
            # Falls Whisper gar nichts erkannt hat
            q_path = os.path.join(BASE_PATH, "Nexus", "_Voice_Queue")
            try:
                err_name = f"{int(time.time())}_Whisper_Err.json"
                err_path = os.path.join(q_path, err_name)
                with open(err_path + ".tmp", "w", encoding="utf-8") as f:
                    json.dump({"text": "Ich habe nichts verstanden.", "owner": "GEE", "voice": "de-DE-KatjaNeural"}, f, ensure_ascii=False)
                os.rename(err_path + ".tmp", err_path)
            except: pass

    except Exception as e:
        print(f"[LARYNX-CRASH] {e}")

        winsound.Beep(300, 1000)
    finally:
        # 3. Butler wieder freigeben & Aufräumen
        if os.path.exists(pause_file): os.remove(pause_file)
        if 'wav_path' in locals() and os.path.exists(wav_path): 
            try: os.remove(wav_path)
            except: pass
        winsound.Beep(800, 200)

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
                        execute_batch("S304_PC_SHUTDOWN.bat")
                    elif any(word in command for word in START_WORDS):
                        execute_batch("S601_ALL_SYSTEMS_GO.bat"); time.sleep(10)
                    elif any(word in command for word in STOP_WORDS):
                        execute_batch("S502_NEXUS_SHUTDOWN.bat"); time.sleep(10)
                    elif any(word in command for word in PAUSE_WORDS):
                        execute_batch("Nexus\\03_PAUSE_VOICE.bat"); time.sleep(2)
                    elif any(word in command for word in RESUME_WORDS):
                        p_file = os.path.join(BASE_PATH, "Nexus", "NEXUS_PAUSE.tmp")
                        # Wir feuern die Batch IMMER, um sicherzugehen
                        execute_batch("Nexus\\04_RESUME_VOICE.bat")
                        print("[EAR] Resume-Impuls gesendet.")
                        time.sleep(2)

                    elif any(word in command for word in SKIP_WORDS):
                        execute_batch("Nexus\\02_NEXT_SPOKE.bat"); time.sleep(2)
                    elif any(word in command for word in SEND_WORDS):
                        pyautogui.press('enter'); winsound.Beep(1200, 100)
        except: time.sleep(0.1)

if __name__ == "__main__":
    winsound.Beep(800, 200); listen_loop()






