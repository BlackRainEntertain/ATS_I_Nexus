import json
import time
import os

# Pfad zur gemeinsamen _Voice_Queue (identisch mit Gee)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
QUEUE_DIR = os.path.join(BASE_DIR, "_Voice_Queue")

def run(message_text):
    if not os.path.exists(QUEUE_DIR):
        os.makedirs(QUEUE_DIR)

    # Grok ist manchmal kürzer angebunden, daher Schwelle auf 3 Zeichen
    if not message_text or len(message_text.strip()) < 3:
        return

    ticket = {
        "owner": "GROK",
        "voice": "de-DE-SeraphinaMultilingualNeural",
        "rate": "-4%",   # Nur minimal schneller als Metas -4%, um den "Grok-Drive" zu halten
        "pitch": "+4Hz", # Der entscheidende Unterschied! Höherer Pitch macht sie präsenter und schärfer
        "text": message_text.strip(),
        "timestamp": time.time()
    }


    # Ticket mit eigenem Namen einwerfen
    file_name = f"{int(time.time()*1000)}_GROK.json"
    file_path = os.path.join(QUEUE_DIR, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(ticket, f, ensure_ascii=False)
