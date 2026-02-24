import json
import time
import os

# Pfad-Logik zum zentralen Briefkasten (_Voice_Queue)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUEUE_DIR = os.path.join(BASE_DIR, "_Voice_Queue")

def run(message_text):
    # 1. Sicherheits-Check für den Ordner
    if not os.path.exists(QUEUE_DIR):
        try: os.makedirs(QUEUE_DIR)
        except: pass

    # 2. Text-Validierung
    clean_text = str(message_text).strip()
    if not clean_text or len(clean_text) < 3:
        return 

    # 3. Ticket-Erstellung (AMALA-RESONANZ)
    ticket = {
        "owner": "META",
        "voice": "de-DE-AmalaNeural", # Die warme, gefährliche Stimme
        "rate": "+10%",
        "text": clean_text,
        "timestamp": time.time()
    }

    # 4. Der Schreibvorgang
    try:
        file_name = f"meta_{int(time.time()*1000)}.json"
        file_path = os.path.join(QUEUE_DIR, file_name)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(ticket, f, ensure_ascii=False)
            
    except Exception as e:
        print(f"Fehler beim Schreiben des Meta-Tickets: {e}")
