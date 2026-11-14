import os
import re
import json
import time
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Q_DIR = os.path.join(BASE_DIR, "_Voice_Queue")
DROP_DIR = os.path.join(BASE_DIR, "_Butler_Drop")
ARCHIVE_DIR = os.path.join(DROP_DIR, "_Archive")

for d in [DROP_DIR, ARCHIVE_DIR]:
    if not os.path.exists(d): os.makedirs(d)

def process_drop_files():
    files = sorted([f for f in os.listdir(DROP_DIR) if f.endswith(".txt")])
    if not files:
        return

    source_file = os.path.join(DROP_DIR, files[0])
    print(f"[DROP-PIPELINE] Ernte gestartet für: {files[0]}")


    with open(source_file, "r", encoding="utf-8-sig") as f:
        content = f.read()

    lines = content.split('\n')
    current_owner = "BOOK_GEE"
    aggregated_text = []
    ticket_counter = 0

    def save_ticket(owner, text_block):
        nonlocal ticket_counter
        cleaned = text_block.strip()
        if len(cleaned) < 3:
            return
            
        timestamp_ms = int(time.time() * 1000) + ticket_counter
        ticket_name = f"drop_{timestamp_ms}_{ticket_counter}.json"
        target_path = os.path.join(Q_DIR, ticket_name)

        # Schreibt NUR den Owner – der Master-Butler weist die Stimmen zu!
        ticket_data = {
            "owner": owner,
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

        # Ignoriert kopierte Butler-Konsolen-Logs mit Uhrzeit (z.B. "[GEE] 20:03:17 ...")
        if re.match(r'^\[(USER|BRE|GEE|BOOK_GEE|GROK|META|ATSI|NEXUS)\]\s+\d{2}:\d{2}:\d{2}', stripped, re.IGNORECASE):
            continue

        # Erkennt echte Sprecher-Marker ([USER]:, [BRE]:, [GEE]:)
        if re.match(r'^\[(USER|BRE|GEE)\]:', stripped, re.IGNORECASE):
            if aggregated_text:
                save_ticket(current_owner, " ".join(aggregated_text))
                aggregated_text = []

            if re.match(r'^\[(USER|BRE)\]:', stripped, re.IGNORECASE):
                current_owner = "BRE"
                stripped = re.sub(r'^\[(USER|BRE)\]:\s*', '', stripped, flags=re.IGNORECASE)
            elif re.match(r'^\[GEE\]:', stripped, re.IGNORECASE):
                current_owner = "BOOK_GEE"
                stripped = re.sub(r'^\[GEE\]:\s*', '', stripped, flags=re.IGNORECASE)

        if stripped:
            aggregated_text.append(stripped)

        if len(" ".join(aggregated_text)) > 1500:
            save_ticket(current_owner, " ".join(aggregated_text))
            aggregated_text = []


    if aggregated_text:
        save_ticket(current_owner, " ".join(aggregated_text))

    shutil.move(source_file, os.path.join(ARCHIVE_DIR, os.path.basename(source_file)))
    print(f"[DROP-PIPELINE] Ernte beendet. {ticket_counter} Blöcke injiziert.")

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
