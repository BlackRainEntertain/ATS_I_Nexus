import json
import time
import os

# Zentrale Pfad-Verankerung im Nexus-Mahlwerk
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUEUE_DIR = os.path.join(BASE_DIR, "_Voice_Queue")

def run(message_text, character_name="AI_TOWN"):
    """
    Kaltstart-Triebwerk für die auditive Identität in AI Town.
    Nutzt das hochflexible Multilingual-Protokoll von Seraphina
    mit einer beruhigten, gesetzten Sprechfrequenz.
    """
    if not os.path.exists(QUEUE_DIR):
        try:
            os.makedirs(QUEUE_DIR)
        except Exception as e:
            print(f"[NEXUS_FATAL] Queue-Verzeichnis konnte nicht erstellt werden: {e}")
            return

    if not message_text or len(message_text.strip()) < 3:
        return

    # --- DAS FINALE MULTILINGUALE HUB-PROTOKOLL ---
    # SeraphinaMultilingual fängt Deutsch und Englisch perfekt ab.
    selected_voice = "de-DE-SeraphinaMultilingualNeural"
    
    # BERUHIGTE FREQUENZ: Von +12% runter auf +2%, damit sie absolut gesetzt und reif spricht.
    selected_rate = "+2%"  

    ticket = {
        "owner": "AI_TOWN",
        "character": character_name,
        "voice": selected_voice,
        "rate": selected_rate,
        "text": message_text.strip(),
        "timestamp": time.time()
    }

    # Formatierung des Tickets für den zentralen Briefkasten
    file_name = f"{int(time.time()*1000)}__AI_TOWN.json"
    file_path = os.path.join(QUEUE_DIR, file_name)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(ticket, f, ensure_ascii=False)
        print(f"[NEXUS_GITHUB] Hub-Ticket gedruckt -> {character_name} via {selected_voice} ({selected_rate})")
    except Exception as e:
        print(f"[NEXUS_ERROR] Fehler beim Schreiben des Hub-Tickets für {character_name}: {e}")



