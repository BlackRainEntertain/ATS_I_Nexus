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
        "voice": "de-CH-LeniNeural",
        "rate": "-15%", # Schweizerdeutsch braucht oft ein bisschen mehr Raum
        "pitch": "-5Hz",
        "text": message_text.strip(),
        "timestamp": time.time()
    }


    # Ticket mit eigenem Namen einwerfen
    file_name = f"{int(time.time()*1000)}_GROK.json"
    file_path = os.path.join(QUEUE_DIR, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(ticket, f, ensure_ascii=False)
