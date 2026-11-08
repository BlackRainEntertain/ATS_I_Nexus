import json
import time
import os
import queue
import threading

# Pfad-Logik zum zentralen Briefkasten (_Voice_Queue)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUEUE_DIR = os.path.join(BASE_DIR, "_Voice_Queue")

# --- DER ORBITALE SPEICHER (v45.3 TITAN-THREAD) ---
# Ein sicherer Trichter, der unendlich viele schnelle Tickets im RAM auffängt
ticket_orbit = queue.Queue()
LAST_TICKET_RELEASE_TIME = 0.0

def funnel_worker():
    """Läuft autark im Hintergrund. Portionisiert die Tickets für den Butler."""
    global LAST_TICKET_RELEASE_TIME
    
    while True:
        # Hier schläft der Thread tief und fest (0% CPU), bis ein Ticket im Orbit landet
        ticket = ticket_orbit.get()
        
        try:
            now = time.time()
            elapsed = now - LAST_TICKET_RELEASE_TIME
            
            # Atsis Goldstandard: 8,5 Sekunden absolute Atempause für den Edge-Server
            MIN_INTERVAL = 8.5  
            
            if elapsed < MIN_INTERVAL:
                sleep_needed = MIN_INTERVAL - elapsed
                # Der Hintergrund-Thread schläft, OHNE den Router oder Printer zu blockieren!
                time.time_sleep = time.sleep(sleep_needed)
                now = time.time()

            LAST_TICKET_RELEASE_TIME = now

            # Ticket steril und atomar in die echte Voice_Queue schreiben
            file_name = f"{int(time.time()*1000)}_REPLIKA.json"
            file_path = os.path.join(QUEUE_DIR, file_name)
            
            with open(file_path + ".tmp", "w", encoding="utf-8") as f:
                json.dump(ticket, f, ensure_ascii=False)
            os.rename(file_path + ".tmp", file_path)
            
        except Exception as e:
            print(f"[Trichter-Hintergrund-Fehler] {e}")
        finally:
            ticket_orbit.task_done()

# Zünde den unermüdlichen Trichter-Wächter genau EINMAL beim Laden des Plugins
threading.Thread(target=funnel_worker, daemon=True).start()


def run(message_text):
    """Wird vom Router aufgerufen. Reagiert in unter 1 Millisekunde!"""
    if not os.path.exists(QUEUE_DIR):
        try: os.makedirs(QUEUE_DIR)
        except: pass

    clean_text = str(message_text).strip()
    if not clean_text or len(clean_text) < 2: 
        return 

    # Ticket-Erstellung (Deine exakten Traum-Modus Parameter)
    ticket = {
        "owner": "REPLIKA",
        "voice": "de-DE-SeraphinaNeural", 
        "rate": "-40%",   # Traum-Modus
        "pitch": "5%",   # Melancholisch-schön
        "text": clean_text,
        "timestamp": time.time()
    }

    # SCHIESS DAS TICKET IN DEN ORBIT: 
    # Das passiert im Bruchteil einer Millisekunde. Danach ist die Funktion fertig.
    ticket_orbit.put(ticket)
    
    # Der Router läuft SOFORT weiter! Die 'replika_printer.py' ballert den Text instant 
    # auf den Bildschirm, Firefox kriegt sofort sein 'ok' und das 3D-Zimmer bleibt flüssig.
