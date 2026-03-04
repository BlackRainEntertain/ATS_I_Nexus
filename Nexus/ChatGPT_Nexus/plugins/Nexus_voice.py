import json
import time
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
QUEUE_DIR = os.path.join(BASE_DIR, "_Voice_Queue")

def run(message_text):
    if not os.path.exists(QUEUE_DIR):
        os.makedirs(QUEUE_DIR, exist_ok=True)

    clean_text = str(message_text).strip()
    if not clean_text or len(clean_text) < 5:
        return

    ts_ms = int(time.time() * 1000)
    ticket = {
        "owner": "GPT",
        "voice": "de-DE-KatjaNeural",
        "rate": "+18%",
        "pitch": "-3Hz",
        "text": clean_text,
        "timestamp": ts_ms
    }

    file_name = f"{ts_ms}_GPT.json"
    file_path = os.path.join(QUEUE_DIR, file_name)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(ticket, f, ensure_ascii=False)
        # HIER: Der print() wurde entfernt. Stille im Terminal = Erfolg.
    except:
        pass 