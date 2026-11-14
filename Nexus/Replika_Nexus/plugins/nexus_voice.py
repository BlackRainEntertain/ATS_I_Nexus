import json
import time
import os
import queue
import threading

# Pfad-Logik zum zentralen Briefkasten (_Voice_Queue)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUEUE_DIR = os.path.join(BASE_DIR, "_Voice_Queue")

# --- DER ORBITALE SPEICHER (v45.4 TITAN-DUPLICATE-FILTER) ---
ticket_orbit = queue.Queue()
LAST_TICKET_RELEASE_TIME = 0.0
LAST_PROCESSED_TEXT = "" # Das Inhalts-Gedächtnis gegen DOM-Doppler

def funnel_worker():
    """Läuft autark im Hintergrund. Blockiert Spam, Duplikate und Zeit-Infarkte."""
    global LAST_TICKET_RELEASE_TIME, LAST_PROCESSED_TEXT
    
    while True:
        ticket = ticket_orbit.get()
        current_text = ticket.get('text', '').strip()
        
        # --- DER INHALTS-SCHUTZSCHILD ---
        if current_text == LAST_PROCESSED_TEXT:
            print(f"[TRICHTER] DOM-Duplikat abgefangen und vernichtet: '{current_text[:30]}...'")
            ticket_orbit.task_done()
            continue
            
        try:
            now = time.time()
            elapsed = now - LAST_TICKET_RELEASE_TIME
            MIN_INTERVAL = 8.5  
            
            if elapsed < MIN_INTERVAL:
                sleep_needed = MIN_INTERVAL - elapsed
                time.sleep(sleep_needed)
                now = time.time()

            LAST_TICKET_RELEASE_TIME = now
            LAST_PROCESSED_TEXT = current_text

            file_name = f"{int(time.time()*1000)}_REPLIKA.json"
            file_path = os.path.join(QUEUE_DIR, file_name)
            
            with open(file_path + ".tmp", "w", encoding="utf-8") as f:
                json.dump(ticket, f, ensure_ascii=False)
            os.rename(file_path + ".tmp", file_path)
            
        except Exception as e:
            print(f"[Trichter-Hintergrund-Fehler] {e}")
        finally:
            ticket_orbit.task_done()

threading.Thread(target=funnel_worker, daemon=True).start()


def run(message_text):
    if not os.path.exists(QUEUE_DIR):
        try: os.makedirs(QUEUE_DIR)
        except: pass

    clean_text = str(message_text).strip()
    if not clean_text or len(clean_text) < 2: 
        return 

    # --- BACKUP ORIGINAL-STIMME (SeraphinaNeural) ---
    # ticket = {
    #     "owner": "REPLIKA",
    #     "voice": "de-DE-SeraphinaNeural", 
    #     "rate": "-40%",   
    #     "pitch": "5%",   
    #     "text": clean_text,
    #     "timestamp": time.time()
    # }

    # --- NEUES SPLIT-SETUP (Sanft & Warm: Leni + Michelle) ---
    ticket = {
        "owner": "REPLIKA",
        "voice_de": "de-CH-LeniNeural",
        "voice_en": "en-US-MichelleNeural",
        "rate_de": "-4%",
        "rate_en": "-4%",
        "pitch_de": "+3Hz",
        "pitch_en": "+2Hz",
        "text": clean_text,
        "timestamp": time.time()
    }

    ticket_orbit.put(ticket)

