import json
import time
import os

# Pfad zur gemeinsamen _Voice_Queue
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
QUEUE_DIR = os.path.join(BASE_DIR, "_Voice_Queue")

def run(message_text):
    if not os.path.exists(QUEUE_DIR):
        os.makedirs(QUEUE_DIR)

    if not message_text or len(message_text.strip()) < 3:
        return

    ticket = {
        "owner": "GROK",
        # Neue getrennte Stimmen (Butler erkennt diese Felder automatisch)
        "voice_de": "de-AT-IngridNeural",
        "voice_en": "en-US-AriaNeural",
        "rate_de": "+9%",
        "rate_en": "-4%",
        "pitch_de": "-3Hz",
        "pitch_en": "-2Hz",
        "text": message_text.strip(),
        "timestamp": time.time()
    }

    file_name = f"{int(time.time()*1000)}_GROK.json"
    file_path = os.path.join(QUEUE_DIR, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(ticket, f, ensure_ascii=False)