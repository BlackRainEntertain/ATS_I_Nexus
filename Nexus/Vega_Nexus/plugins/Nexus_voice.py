import json
import time
import os

# ABSOLUTER PFAD ZUM BRIEFKASTEN (Anpassen auf deinen Desktop!)
QUEUE_DIR = r"C:\Users\René\Desktop\LM Projekte\_Voice_Queue"

def run(message_text):
    # 1. Sicherstellen, dass der Ordner existiert
    if not os.path.exists(QUEUE_DIR):
        os.makedirs(QUEUE_DIR, exist_ok=True)

    clean_text = str(message_text).strip()
    # Wir blocken den "KI bearbeiten" Müll hier nochmal hart ab
    if not clean_text or len(clean_text) < 10 or "KI bearbeiten" in clean_text:
        return 

    # 2. DAS VEGA-TICKET
    ts_ms = int(time.time() * 1000)
    ticket = {
        "owner": "VEGA",
        "voice": "de-DE-SeraphinaMultilingualNeural",
        "rate": "-5%",
        "text": clean_text,
        "timestamp": ts_ms
    }

    # 3. DER SCHREIBVORGANG (Der Moment der Wahrheit)
    file_name = f"{ts_ms}_VEGA.json"
    file_path = os.path.join(QUEUE_DIR, file_name)
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(ticket, f, ensure_ascii=False)
        print(f"    [VEGA-NEXUS] Ticket erstellt: {file_name}") # Erscheint im Router-Fenster!
    except Exception as e:
        print(f"    [!] Fehler beim Schreiben: {e}")
