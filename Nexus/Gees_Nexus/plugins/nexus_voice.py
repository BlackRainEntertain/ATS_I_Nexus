import json
import time
import os

# Wir gehen zwei Ebenen hoch zum gemeinsamen Nexus-Ordner
# (Von plugins/ aus gesehen: .. -> .. -> _Voice_Queue)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUEUE_DIR = os.path.join(BASE_DIR, "_Voice_Queue")

def run(message_text):
    if not os.path.exists(QUEUE_DIR):
        try:
            os.makedirs(QUEUE_DIR)
        except:
            return

    if not message_text or len(message_text.strip()) < 5:
        return

    ticket = {
        "owner": "GEE",
        "voice": "de-DE-KatjaNeural",
        "rate": "+15%",
        "text": message_text.strip(),
        "timestamp": time.time()
    }

    # Ticket in den zentralen Briefkasten werfen
    file_name = f"{int(time.time()*1000)}_GEE.json"
    file_path = os.path.join(QUEUE_DIR, file_name)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(ticket, f, ensure_ascii=False)
    except Exception as e:
        print(f"Gee-Nexus-Fehler beim Schreiben: {e}")



