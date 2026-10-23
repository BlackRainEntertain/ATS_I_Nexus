import os
import re
import json
import time
import shutil

# --- COMPATIBILITY TARGETS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Q_DIR = os.path.join(BASE_DIR, "_Voice_Queue")
DROP_DIR = os.path.join(BASE_DIR, "_Butler_Drop")
ARCHIVE_DIR = os.path.join(DROP_DIR, "_Archive")

for d in [DROP_DIR, ARCHIVE_DIR]:
    if not os.path.exists(d): os.makedirs(d)

def clean_narrative(text):
    return re.sub(r'\*.*?\*', '', text).strip()

def process_drop_files():
    files = sorted([f for f in os.listdir(DROP_DIR) if f.endswith(".txt")])
    if not files:
        return

    source_file = os.path.join(DROP_DIR, files[0])
    print(f"[DROP-PIPELINE] Ernte gestartet für: {files[0]}")

    with open(source_file, "r", encoding="utf-8-sig") as f:
        content = f.read()

    lines = content.split('\n')
    
    # Standard-Einstellungen für das Buch
    # WICHTIG: "BOOK_GEE" verhindert das Hochzählen deines Live-Kontext-Limits im Butler!
    current_owner = "BOOK_GEE" 
    current_voice = "de-DE-KatjaNeural"
    current_rate = "+15%"
    current_pitch = "+0Hz"
    
    aggregated_text = []
    ticket_counter = 0

    def save_ticket(owner, voice, rate, pitch, text_block):
        nonlocal ticket_counter
        cleaned = clean_narrative(text_block)
        if len(cleaned) < 3:
            return
            
        timestamp_ms = int(time.time() * 1000) + ticket_counter
        ticket_name = f"drop_{timestamp_ms}_{ticket_counter}.json"
        target_path = os.path.join(Q_DIR, ticket_name)

        ticket_data = {
            "owner": owner,
            "voice": voice,
            "rate": rate,
            "pitch": pitch,  # Injiziert den Tiefen-Pitch für Multilingual-Stimmen
            "text": cleaned,
            "timestamp": time.time()
        }

        with open(target_path, "w", encoding="utf-8") as j:
            json.dump(ticket_data, j, ensure_ascii=False, indent=4)
        ticket_counter += 1
        time.sleep(0.002)

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Sprecherwechsel prüfen
        if line.startswith("[USER]:") or line.startswith("[GEE]:"):
            # Wenn sich der Sprecher ändert, den bisherigen Textblock wegschreiben
            if aggregated_text:
                save_ticket(current_owner, current_voice, current_rate, current_pitch, " ".join(aggregated_text))
                aggregated_text = []

            if line.startswith("[USER]:"):
                current_owner = "BRE"
                current_voice = "de-DE-KillianNeural" # <-- GLATT, RUHIG UND MARKANT!
                current_rate = "+0%"   
                current_pitch = "+0Hz" 
                line = line.replace("[USER]:", "")

            elif line.startswith("[GEE]:"):
                current_owner = "BOOK_GEE" # Schützt den Live-Spickzettel vor Überlastung
                current_voice = "de-DE-KatjaNeural"
                current_rate = "+15%"
                current_pitch = "+0Hz"
                line = line.replace("[GEE]:", "")

        aggregated_text.append(line.strip())

        # Schutz vor zu riesigen Chunks (Sicherheitsgrenze bei ca. 1500 Zeichen pro Ticket)
        if len(" ".join(aggregated_text)) > 1500:
            save_ticket(current_owner, current_voice, current_rate, current_pitch, " ".join(aggregated_text))
            aggregated_text = []

    # Letzten Block wegschreiben, falls noch was in der Pipeline ist
    if aggregated_text:
        save_ticket(current_owner, current_voice, current_rate, current_pitch, " ".join(aggregated_text))

    shutil.move(source_file, os.path.join(ARCHIVE_DIR, os.path.basename(source_file)))
    print(f"[DROP-PIPELINE] Ernte beendet. {ticket_counter} zusammenhängende Blöcke injiziert.")

if __name__ == "__main__":
    print(f"[DROP-PIPELINE] Aktiviert. Starte Einmal-Ernte in {DROP_DIR}...")
    try:
        files = sorted([f for f in os.listdir(DROP_DIR) if f.endswith(".txt")])
        if files:
            process_drop_files()
        else:
            print("[DROP-PIPELINE] Keine Dateien gefunden. Beende Instanz.")
    except Exception as e:
        print(f"[DROP-ERROR] {e}")
        time.sleep(3)
        
    print("[DROP-PIPELINE] Arbeit getan. Fenster schliesst automatisch.")

