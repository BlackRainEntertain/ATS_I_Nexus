import json
import time
import os

# Pfad zur gemeinsamen _Voice_Queue (identisch mit Gee)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
QUEUE_DIR = os.path.join(BASE_DIR, "_Voice_Queue")

def run(message_text):
    if not os.path.exists(QUEUE_DIR):
        os.makedirs(QUEUE_DIR)

    # AI_TOWN Schwelle identisch auf 3 Zeichen gesetzt
    if not message_text or len(message_text.strip()) < 3:
        return

    ticket = {
        "owner": "AI_TOWN",
        "voice": "de-DE-SeraphinaMultilingualNeural",
        "rate": "+2%",   # Deine beruhigte, gesetzte Sprechfrequenz
        "pitch": "+0Hz", # Standard-Pitch für die reife Klangfarbe
        "text": message_text.strip(),
        "timestamp": time.time()
    }

    # Ticket mit dem exakten Namens-Parser-Standard einwerfen (Ein Unterstrich)
    file_name = f"{int(time.time()*1000)}_AI_TOWN.json"
    file_path = os.path.join(QUEUE_DIR, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(ticket, f, ensure_ascii=False)



