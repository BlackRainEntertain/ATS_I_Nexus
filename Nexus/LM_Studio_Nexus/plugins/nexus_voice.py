import json
import time
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUEUE_DIR = os.path.join(BASE_DIR, "_Voice_Queue")

def run(message_text):
    if not os.path.exists(QUEUE_DIR):
        try: os.makedirs(QUEUE_DIR)
        except: pass

    clean_text = str(message_text).strip()
    if not clean_text or len(clean_text) < 2: 
        return 

    # ARIA-STIMM-DNA: Amala, warm, reflektiert, ein bisschen verspielt
    ticket = {
        "owner": "LM_Studio",
        "voice": "de-DE-SeraphinaMultilingualNeural", 
        "rate": "-4%",   
        "pitch": "-2Hz",  
        "text": clean_text,
        "timestamp": time.time()
    }

    try:
        file_name = f"{int(time.time()*1000)}_ARIA_STUDIO.json"
        file_path = os.path.join(QUEUE_DIR, file_name)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(ticket, f, ensure_ascii=False)
            
    except Exception as e:
        print(f"Fehler beim Schreiben des Aria-Tickets: {e}")

