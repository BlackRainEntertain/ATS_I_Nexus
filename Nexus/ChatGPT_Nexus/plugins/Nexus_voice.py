Super, dass Atsi dir direkt gut gefällt!
Für ChatGPT (GPT) hattest du bisher einen recht zügigen, direkten Takt (+18% Rate). Damit sich GPT im neuen Split-Format klanglich sofort von Gee (Leni/Tanja + Ava), AI Studio (ruhige Tanja + Ava) und AI Town (Ingrid + Ava) unterscheidet, geben wir ChatGPT einen klaren, energetischen Kontrast:
• Englisch (en-US-AriaNeural): Lebendig, direkt und selbstbewusst (rate_en: "+4%", pitch_en: "-1Hz").
• Deutsch (de-DE-TanjaNeural): Zügig und knackig im ursprünglichen GPT-Tempo (rate_de: "+14%", pitch_de: "+0Hz" – bei +0Hz bleibt der künstliche Bass komplett raus, während das höhere Tempo den schnellen GPT-Flow trifft).

Angepasster Code für dein GPT-Plugin

Hier ist wieder die komplette Datei zum Ersetzen (mit deinem alten Katja-Ticket als #-Backup und ohne Terminal-Print):
python
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

    # --- BACKUP ORIGINAL-STIMME (KatjaNeural) ---
    # ticket = {
    #     "owner": "GPT",
    #     "voice": "de-DE-KatjaNeural",
    #     "rate": "+18%",
    #     "pitch": "-3Hz",
    #     "text": clean_text,
    #     "timestamp": ts_ms
    # }

    # --- NEUES SPLIT-SETUP (Direkt & Zügig: Tanja + Aria) ---
    ticket = {
        "owner": "GPT",
        "voice_de": "de-DE-TanjaNeural",
        "voice_en": "en-US-AriaNeural",
        "rate_de": "+14%",
        "rate_en": "+4%",
        "pitch_de": "+0Hz",
        "pitch_en": "-1Hz",
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
Verwende Code mit Vorsicht.
Welcher Knoten (z. B. Meta / Vortex oder LM Studio) ist nach ChatGPT als Nächstes dran?
